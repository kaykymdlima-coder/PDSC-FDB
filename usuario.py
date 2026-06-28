from conexao import Session
from models import UsuarioPessoa, UsuarioDoador, UsuarioPaciente

def inserir_usuario(dados, tipo_perfil="Pessoa Comum", dados_extras=None):
    session = SessionLocal()
    try:
        # 1. Sempre insere primeiro na tabela pai (UsuarioPessoa)
        novo_usuario = UsuarioPessoa(
            cpf=dados["cpf"],
            nome_completo=dados["nome_completo"],
            data_nascimento=dados["data_nascimento"],
            email=dados["email"],
            senha=dados["senha"],
            sexo=dados["sexo"],
            tipo_sanguineo=dados["tipo_sanguineo"],
            logradouro=dados["logradouro"],
            cidade=dados["cidade"],
            bairro=dados["bairro"],
            cep=dados["cep"],
            telefone=dados["telefone"]
        )
        session.add(novo_usuario)
        session.flush() # Envia ao banco para garantir que o CPF exista antes das próximas inserções

        # 2. Insere na tabela correspondente ao perfil selecionado
        if tipo_perfil == "Doador" and dados_extras:
            novo_doador = UsuarioDoador(
                id_doador=dados_extras["id_doador"],
                cpf=dados["cpf"],
                pontuacao=dados_extras.get("pontuacao", 0),
                id_campanha=dados_extras["id_campanha"]
            )
            session.add(novo_doador)
            
        elif tipo_perfil == "Paciente" and dados_extras:
            novo_paciente = UsuarioPaciente(
                id_paciente=dados_extras["id_paciente"],
                cpf=dados["cpf"],
                data_entrada_fila=dados_extras["data_entrada_fila"],
                id_instituicao=dados_extras["id_instituicao"]
            )
            session.add(novo_paciente)

        session.commit()
        print(f"Usuário ({tipo_perfil}) cadastrado com sucesso!")
    except Exception as e:
        session.rollback()
        print(f"Erro ao inserir: {e}")
        raise e
    finally:
        session.close()

def editar_usuario(cpf, dados):
    session = SessionLocal()
    try:
        usuario = session.query(UsuarioPessoa).filter(UsuarioPessoa.cpf == cpf).first()
        if usuario:
            for chave, valor in dados.items():
                if hasattr(usuario, chave) and valor:
                    setattr(usuario, chave, valor)
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def remover_usuario(cpf):
    session = SessionLocal()
    try:
        # Remove primeiro das tabelas filhas para evitar erros de chave estrangeira
        session.query(UsuarioDoador).filter(UsuarioDoador.cpf == cpf).delete()
        session.query(UsuarioPaciente).filter(UsuarioPaciente.cpf == cpf).delete()
        # Remove da tabela pai
        session.query(UsuarioPessoa).filter(UsuarioPessoa.cpf == cpf).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def listar_usuarios(tipo_perfil="Pessoa Comum"):
    session = SessionLocal()
    try:
        if tipo_perfil == "Doador":
            # Faz um JOIN entre UsuarioPessoa e UsuarioDoador
            resultados = session.query(UsuarioPessoa, UsuarioDoador).join(UsuarioDoador, UsuarioPessoa.cpf == UsuarioDoador.cpf).all()
            return resultados
        elif tipo_perfil == "Paciente":
            # Faz um JOIN entre UsuarioPessoa e UsuarioPaciente
            resultados = session.query(UsuarioPessoa, UsuarioPaciente).join(UsuarioPaciente, UsuarioPessoa.cpf == UsuarioPaciente.cpf).all()
            return resultados
        else:
            return session.query(UsuarioPessoa).all()
    finally:
        session.close()