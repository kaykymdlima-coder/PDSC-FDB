from conexao import Session
from models import UsuarioPessoa


def listar_usuarios():

    session = Session()

    usuarios = session.query(UsuarioPessoa).all()

    session.close()

    return usuarios