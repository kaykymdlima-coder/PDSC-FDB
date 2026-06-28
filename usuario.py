from conexao import Session
from models import UsuarioPessoa

def inserir_usuario(dados_usuario):
    session = Session()
    novo_usuario = UsuarioPessoa(**dados_usuario)
    session.add(novo_usuario)
    session.commit()
    session.close()

def editar_usuario(cpf, novos_dados):
    session = Session()
    usuario = session.query(UsuarioPessoa).filter_by(cpf=cpf).first()
    if usuario:
        for campo, valor in novos_dados.items():
            if hasattr(usuario, campo):
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