import os
from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename
from models.models import Pessoa, Imagem, db
from services.face_service import get_face_encoding, serialize_encoding

pessoas_bp = Blueprint('pessoas', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@pessoas_bp.route('/pessoas')
@login_required
def listar_pessoas():
    pessoas = Pessoa.query.all()
    # Adicionar contagem de imagens
    for pessoa in pessoas:
        pessoa.qtd_fotos = Imagem.query.filter_by(pessoa_id=pessoa.id).count()
    return render_template('pessoas.html', pessoas=pessoas)

@pessoas_bp.route('/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        
        if not nome or not cpf:
            flash('Nome e CPF são obrigatórios.', 'danger')
            return render_template('cadastro.html')
            
        # Verificar se CPF já existe
        if Pessoa.query.filter_by(cpf=cpf).first():
            flash('CPF já cadastrado.', 'danger')
            return render_template('cadastro.html')

        files = request.files.getlist('fotos')
        if not files or files[0].filename == '':
            flash('Pelo menos uma foto é obrigatória.', 'danger')
            return render_template('cadastro.html')

        nova_pessoa = Pessoa(nome=nome, cpf=cpf)
        db.session.add(nova_pessoa)
        db.session.commit()

        encoding_salvo = False
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                # Para evitar nomes duplicados
                ext = filename.rsplit('.', 1)[1].lower()
                new_filename = f"pessoa_{nova_pessoa.id}_{len(nova_pessoa.imagens)}_{filename}"
                filepath = os.path.join(upload_folder, new_filename)
                
                file.save(filepath)
                
                # Salvar no banco
                img_record = Imagem(pessoa_id=nova_pessoa.id, caminho_imagem=f"uploads/{new_filename}")
                db.session.add(img_record)
                
                # Extrair encoding da primeira foto válida para cadastro facial
                if not encoding_salvo:
                    encoding = get_face_encoding(filepath)
                    if encoding is not None:
                        nova_pessoa.encoding_facial = serialize_encoding(encoding)
                        encoding_salvo = True

        if not encoding_salvo:
            db.session.rollback()
            flash('Nenhum rosto detectado nas imagens. Cadastro cancelado.', 'danger')
            # Opcionalmente deletar imagens...
            return render_template('cadastro.html')
            
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        # Redireciona para listar as pessoas via o url correto. Como a função está no mesmo blueprint, 'pessoas.listar_pessoas' é o endpoint.
        # Mas para simplificar, redirecionamos via URL hardcoded.
        from flask import redirect
        return redirect('/pessoas')

    return render_template('cadastro.html')

@pessoas_bp.route('/pessoas/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    # Arquivos físicos também poderiam ser removidos aqui
    db.session.delete(pessoa)
    db.session.commit()
    flash('Pessoa excluída com sucesso.', 'success')
    from flask import redirect
    return redirect('/pessoas')
