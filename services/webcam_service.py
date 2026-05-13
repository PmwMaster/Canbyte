import cv2
import face_recognition
from services.face_service import process_base64_image, get_face_encoding_from_cv2
from services.recognition_service import identify_person

def process_webcam_frame(base64_image):
    """
    Processa um frame recebido da webcam via base64.
    Retorna dados da pessoa reconhecida ou None.
    """
    # Converter de base64 para imagem OpenCV
    cv2_img = process_base64_image(base64_image)
    
    if cv2_img is None:
        return {"success": False, "message": "Imagem inválida"}

    # Extrair encoding
    encoding = get_face_encoding_from_cv2(cv2_img)
    
    if encoding is None:
        return {"success": False, "message": "Nenhum rosto detectado"}

    # Identificar pessoa
    pessoa, confianca = identify_person(encoding)
    
    if pessoa:
        # Nota: Só salva no histórico periodicamente para não floodar o BD. 
        # A lógica de salvar pode ficar na rota.
        return {
            "success": True, 
            "pessoa_id": pessoa.id,
            "nome": pessoa.nome,
            "confianca": confianca
        }
    else:
        return {"success": False, "message": "Pessoa não identificada"}
