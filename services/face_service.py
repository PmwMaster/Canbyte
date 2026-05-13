import cv2
import face_recognition
import numpy as np
import json
import base64

def get_face_encoding(image_path):
    """
    Carrega a imagem, detecta rosto e retorna o encoding facial.
    Retorna None se nenhum rosto for detectado.
    """
    try:
        # Carrega a imagem
        image = face_recognition.load_image_file(image_path)
        
        # Encontra todos os rostos na imagem
        face_locations = face_recognition.face_locations(image)
        
        if not face_locations:
            return None
            
        # Pega o encoding do primeiro rosto encontrado
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        if face_encodings:
            return face_encodings[0]
        return None
    except Exception as e:
        print(f"Erro ao extrair encoding de {image_path}: {e}")
        return None

def find_faces_in_image(image_path):
    """
    Encontra todas as localizações e encodings de rostos numa imagem.
    """
    try:
        image = face_recognition.load_image_file(image_path)
        # Converter para RGB (face_recognition usa RGB)
        # O load_image_file já carrega como RGB através do PIL/imageio
        
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        return face_locations, face_encodings, image
    except Exception as e:
        print(f"Erro ao processar imagem para busca: {e}")
        return [], [], None

def serialize_encoding(encoding):
    """Converte numpy array para JSON string"""
    if encoding is None:
        return None
    return json.dumps(encoding.tolist())

def deserialize_encoding(encoding_json):
    """Converte JSON string para numpy array"""
    if not encoding_json:
        return None
    try:
        return np.array(json.loads(encoding_json))
    except Exception:
        return None

def process_base64_image(base64_string):
    """
    Converte uma string base64 (gerada pelo canvas do frontend) em uma imagem do OpenCV.
    """
    try:
        # Remove o cabeçalho "data:image/jpeg;base64,"
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
            
        # Decodifica base64 para bytes
        img_data = base64.b64decode(base64_string)
        
        # Converte bytes para array numpy
        nparr = np.frombuffer(img_data, np.uint8)
        
        # Decodifica array numpy em formato de imagem (BGR)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(f"Erro ao processar imagem base64: {e}")
        return None

def get_face_encoding_from_cv2(cv2_img):
    """
    Obtém o encoding de uma imagem no formato do OpenCV (BGR).
    """
    try:
        # face_recognition trabalha com RGB
        rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_img)
        if not face_locations:
            return None
            
        face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
        if face_encodings:
            return face_encodings[0]
        return None
    except Exception as e:
        print(f"Erro ao extrair encoding do frame da webcam: {e}")
        return None
