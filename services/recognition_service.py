import face_recognition
import numpy as np
from models.models import Pessoa, HistoricoReconhecimento, db
from services.face_service import deserialize_encoding
from datetime import datetime

def identify_person(unknown_encoding, tolerance=0.5):
    """
    Compara o encoding desconhecido com os encodings no banco de dados.
    Retorna (Pessoa, confianca) ou (None, 0).
    """
    if unknown_encoding is None:
        return None, 0.0

    pessoas = Pessoa.query.all()
    
    if not pessoas:
        return None, 0.0

    best_match = None
    best_confidence = 0.0
    min_distance = 1.0 # Menor distância = maior similaridade

    for pessoa in pessoas:
        if not pessoa.encoding_facial:
            continue
            
        known_encoding = deserialize_encoding(pessoa.encoding_facial)
        if known_encoding is None:
            continue

        # Calcula a distância (quanto menor, mais parecidos)
        face_distances = face_recognition.face_distance([known_encoding], unknown_encoding)
        distance = face_distances[0]
        
        if distance < tolerance and distance < min_distance:
            min_distance = distance
            best_match = pessoa
            
            # Converte distância para um percentual de confiança
            # Distância de 0.0 -> 100%
            # Distância de tolerance (0.5) -> 50%
            # formula simplificada
            best_confidence = round((1.0 - distance) * 100, 2)

    return best_match, best_confidence

def save_history(pessoa_id, confianca, origem):
    """
    Salva o registro do reconhecimento no banco.
    """
    try:
        historico = HistoricoReconhecimento(
            pessoa_id=pessoa_id,
            confianca=confianca,
            origem=origem
        )
        db.session.add(historico)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar histórico: {e}")
