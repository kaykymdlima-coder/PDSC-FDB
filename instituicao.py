from conexao import Session
from models import Instituicao
from sqlalchemy.exc import IntegrityError
from typing import Optional, Dict, Any, List


def listar_instituicoes() -> List[Dict[str, Any]]:
    """Retorna lista de dicionários com todos os dados das instituições."""
    with Session() as session:
        instituicoes = session.query(Instituicao).all()
        return [
            {
                "id_instituicao": i.id_instituicao,
                "cnpj": i.cnpj,
                "nome": i.nome,
                "registro_cnes": i.registro_cnes,
                "telefone_institucional": i.telefone_institucional,
                "email_institucional": i.email_institucional,
                "senha": i.senha,
                "cep": i.cep,
                "logradouro": i.logradouro,
                "cidade": i.cidade,
                "bairro": i.bairro,
            }
            for i in instituicoes
        ]


def adicionar_instituicao(dados: Dict[str, Any]) -> bool:
    """
    Insere uma nova instituição.
    Espera as chaves: id_instituicao, cnpj, nome, registro_cnes,
    telefone_institucional, email_institucional, senha, cep,
    logradouro, cidade, bairro.
    Retorna True se OK, False caso contrário.
    """
    try:
        with Session() as session:
            nova = Instituicao(
                id_instituicao=dados["id_instituicao"],
                cnpj=dados["cnpj"],
                nome=dados["nome"],
                registro_cnes=dados["registro_cnes"],
                telefone_institucional=dados["telefone_institucional"],
                email_institucional=dados["email_institucional"],
                senha=dados["senha"],
                cep=dados["cep"],
                logradouro=dados["logradouro"],
                cidade=dados["cidade"],
                bairro=dados["bairro"],
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


def editar_instituicao(id_instituicao: int, dados: Dict[str, Any]) -> bool:
    """Atualiza uma instituição existente. Retorna True se OK."""
    try:
        with Session() as session:
            instituicao = session.query(Instituicao).filter_by(id_instituicao=id_instituicao).first()
            if not instituicao:
                return False
            # Atualiza apenas os campos fornecidos
            for key, value in dados.items():
                if hasattr(instituicao, key) and key != "id_instituicao":
                    setattr(instituicao, key, value)
            session.commit()
            return True
    except Exception as e:
        print(f"Erro ao editar: {e}")
        return False


def excluir_instituicao(id_instituicao: int) -> bool:
    """Remove uma instituição. Retorna True se OK."""
    try:
        with Session() as session:
            instituicao = session.query(Instituicao).filter_by(id_instituicao=id_instituicao).first()
            if not instituicao:
                return False
            session.delete(instituicao)
            session.commit()
            return True
    except Exception as e:
        print(f"Erro ao excluir: {e}")
        return False


def obter_instituicao_por_id(id_instituicao: int) -> Optional[Dict[str, Any]]:
    """Retorna os dados de uma instituição específica ou None."""
    with Session() as session:
        i = session.query(Instituicao).filter_by(id_instituicao=id_instituicao).first()
        if not i:
            return None
        return {
            "id_instituicao": i.id_instituicao,
            "cnpj": i.cnpj,
            "nome": i.nome,
            "registro_cnes": i.registro_cnes,
            "telefone_institucional": i.telefone_institucional,
            "email_institucional": i.email_institucional,
            "senha": i.senha,
            "cep": i.cep,
            "logradouro": i.logradouro,
            "cidade": i.cidade,
            "bairro": i.bairro,
        }