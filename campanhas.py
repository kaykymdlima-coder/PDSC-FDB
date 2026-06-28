from banco import Session
from models import Campanha, Instituicao
from sqlalchemy.exc import IntegrityError
from datetime import date
from typing import Optional, Dict, Any, List


def listar_instituicoes() -> List[Dict[int, str]]:
    with Session() as session:
        instituicoes = session.query(Instituicao).all()
        return [{"id": i.id_instituicao, "nome": i.nome} for i in instituicoes]