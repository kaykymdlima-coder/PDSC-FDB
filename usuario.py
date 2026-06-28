from conexao import Session
from models import UsuarioPessoa

def inserir_usuario(...):
    session = Session()

    session.add(usuario)
    session.commit()

    session.close()

def editar_usuario(cpf, ...):
    session = Session()

    usuario = session.query(UsuarioPessoa).filter_by(cpf=cpf).first()
    if usuario:
        for campo, valor in dados.items():
            setattr(usuario, campo, valor)

        session.commit()

    session.close()

def remover_usuario(cpf):
    session = Session()

    usuario = session.query(UsuarioPessoa).filter_by(cpf=cpf).first()

    if usuario:
        session.delete(usuario)
        session.commit()

    session.close()
def listar_usuarios():

    session = Session()

    usuarios = session.query(UsuarioPessoa).all()

    session.close()
    return usuarios