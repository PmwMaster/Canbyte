import os
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
from services.webcam_service import process_webcam_frame
from services.face_service import get_face_encoding
from services.recognition_service import identify_person, save_history
from routes.pessoas import allowed_file

reconhecimento_bp = Blueprint('reconhecimento', __name__)

@reconhecimento_bp.route('/webcam')
def webcam():
    return render_template('webcam.html')

@reconhecimento_bp.route('/api/reconhecer/frame', methods=['POST'])
def reconhecer_frame():
    data = request.json
    if not data or 'image' not in data:
        return jsonify({"success": False, "message": "Nenhuma imagem recebida"}), 400
        
    base64_image = data['image']
    resultado = process_webcam_frame(base64_image)
    
    # Se reconheceu, salvar no histórico (de forma rate-limited na vida real, aqui salvamos)
    if resultado.get("success") and "pessoa_id" in resultado:
        save_history(resultado["pessoa_id"], resultado["confianca"], "webcam")
        
    return jsonify(resultado)

@reconhecimento_bp.route('/upload-reconhecimento', methods=['GET', 'POST'])
def upload_reconhecimento():
    if request.method == 'POST':
        if 'foto' not in request.files:
            return jsonify({"success": False, "message": "Nenhum arquivo"}), 400
            
        file = request.files['foto']
        if file.filename == '':
            return jsonify({"success": False, "message": "Nenhum arquivo selecionado"}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'temp')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            
            encoding = get_face_encoding(filepath)
            
            if encoding is None:
                os.remove(filepath)
                return jsonify({"success": False, "message": "Nenhum rosto detectado na imagem."})
                
            pessoa, confianca = identify_person(encoding)
            
            # Limpa temp
            os.remove(filepath)
            
            if pessoa:
                save_history(pessoa.id, confianca, "upload")
                return jsonify({
                    "success": True, 
                    "nome": pessoa.nome, 
                    "confianca": confianca,
                    "cpf": pessoa.cpf
                })
            else:
                return jsonify({"success": False, "message": "Pessoa não identificada no banco de dados."})
                
    return render_template('upload_reconhecimento.html')
