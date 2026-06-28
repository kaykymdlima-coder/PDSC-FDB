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


def adicionar_campanha(dados: Dict[str, Any]) -> bool:
    try:
        with Session() as session:
            nova = Campanha(
                id_campanha=dados["id_campanha"],
                nome=dados["nome"],
                regiao=dados["regiao"],
                data_inicio=dados["data_inicio"],
                data_fim=dados["data_fim"],
                status=dados["status"],
                redes_sociais=dados.get("redes_sociais"),
                id_instituicao=dados["id_instituicao"],
            )
            session.add(nova)
            session.commit()
            return True
    except IntegrityError as e:
        print(f"Erro de integridade: {e}")
        return False
    except Exception as e:
        print(f"Erro ao adicionar: {e}")
        return False


def editar_campanha(id_campanha: int, dados: Dict[str, Any]) -> bool:
    """Atualiza uma campanha existente. Retorna True se OK."""
    try:
        with Session() as session:
            campanha = session.query(Campanha).filter_by(id_campanha=id_campanha).first()
            if not campanha:
                return False
            # Atualiza apenas os campos fornecidos
            for key, value in dados.items():
                if hasattr(campanha, key):
                    setattr(campanha, key, value)
            session.commit()
            return True
    except Exception as e:
        print(f"Erro ao editar: {e}")
        return False


def excluir_campanha(id_campanha: int) -> bool:
    """Remove uma campanha. Retorna True se OK."""
    try:
        with Session() as session:
            campanha = session.query(Campanha).filter_by(id_campanha=id_campanha).first()
            if not campanha:
                return False
            session.delete(campanha)
            session.commit()
            return True
    except Exception as e:
        print(f"Erro ao excluir: {e}")
        return False


def obter_campanha_por_id(id_campanha: int) -> Optional[Dict[str, Any]]:
    """Retorna os dados de uma campanha específica ou None."""
    with Session() as session:
        c = session.query(Campanha).filter_by(id_campanha=id_campanha).first()
        if not c:
            return None
        return {
            "id_campanha": c.id_campanha,
            "nome": c.nome,
            "regiao": c.regiao,
            "data_inicio": c.data_inicio,
            "data_fim": c.data_fim,
            "status": c.status,
            "redes_sociais": c.redes_sociais,
            "id_instituicao": c.id_instituicao,
        }