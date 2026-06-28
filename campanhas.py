from banco import Session
from models import Campanha, Instituicao
from sqlalchemy.exc import IntegrityError
from datetime import date
from typing import Optional, Dict, Any, List


def listar_instituicoes() -> List[Dict[int, str]]:
    with Session() as session:
        instituicoes = session.query(Instituicao).all()
        return [{"id": i.id_instituicao, "nome": i.nome} for i in instituicoes]


def listar_campanhas() -> List[Dict[str, Any]]:
    """Retorna lista de dicionários com todos os dados das campanhas."""
    with Session() as session:
        campanhas = session.query(Campanha).all()
        return [
            {
                "id_campanha": c.id_campanha,
                "nome": c.nome,
                "regiao": c.regiao,
                "data_inicio": c.data_inicio,
                "data_fim": c.data_fim,
                "status": c.status,
                "redes_sociais": c.redes_sociais,
                "id_instituicao": c.id_instituicao,
            }
            for c in campanhas
        ]