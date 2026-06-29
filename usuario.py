from conexao import Session
from sqlalchemy.exc import IntegrityError
from models import UsuarioPessoa, UsuarioDoador, UsuarioPaciente


def _serialize_model(model):
    return {key: value for key, value in model.__dict__.items() if key != '_sa_instance_state'}


def inserir_usuario(dados, tipo_perfil='Pessoa Comum', dados_extras=None):
    session = Session()
    try:
        novo_usuario = UsuarioPessoa(
            cpf=dados['cpf'],
            nome_completo=dados['nome_completo'],
            data_nascimento=dados['data_nascimento'],
            email=dados['email'],
            senha=dados['senha'],
            sexo=dados['sexo'],
            tipo_sanguineo=dados['tipo_sanguineo'],
            logradouro=dados['logradouro'],
            cidade=dados['cidade'],
            bairro=dados['bairro'],
            cep=dados['cep'],
            telefone=dados['telefone'],
        )
        session.add(novo_usuario)
        session.flush()

        if tipo_perfil == 'Doador' and dados_extras:
            novo_doador = UsuarioDoador(
                id_doador=int(dados_extras['id_doador']),
                cpf=dados['cpf'],
                pontuacao=int(dados_extras.get('pontuacao', 0)),
                id_campanha=int(dados_extras['id_campanha']),
            )
            session.add(novo_doador)
        elif tipo_perfil == 'Paciente' and dados_extras:
            novo_paciente = UsuarioPaciente(
                id_paciente=int(dados_extras['id_paciente']),
                cpf=dados['cpf'],
                data_entrada_fila=dados_extras['data_entrada_fila'],
                id_instituicao=int(dados_extras['id_instituicao']),
            )
            session.add(novo_paciente)

        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def editar_usuario(cpf, dados):
    session = Session()
    try:
        usuario = session.query(UsuarioPessoa).filter(UsuarioPessoa.cpf == cpf).first()
        if not usuario:
            return False
        for chave, valor in dados.items():
            if valor is not None and valor != '' and hasattr(usuario, chave):
                setattr(usuario, chave, valor)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def remover_usuario(cpf):
    session = Session()
    try:
        removidos = 0
        removidos += session.query(UsuarioDoador).filter(UsuarioDoador.cpf == cpf).delete()
        removidos += session.query(UsuarioPaciente).filter(UsuarioPaciente.cpf == cpf).delete()
        removidos += session.query(UsuarioPessoa).filter(UsuarioPessoa.cpf == cpf).delete()
        session.commit()
        return removidos > 0
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def listar_usuarios(tipo_perfil='Pessoa Comum'):
    session = Session()
    try:
        if tipo_perfil == 'Doador':
            resultados = session.query(UsuarioPessoa, UsuarioDoador).join(
                UsuarioDoador, UsuarioPessoa.cpf == UsuarioDoador.cpf
            ).all()
            return [
                {
                    'cpf': pessoa.cpf,
                    'nome_completo': pessoa.nome_completo,
                    'email': pessoa.email,
                    'cidade': pessoa.cidade,
                    'tipo_sanguineo': pessoa.tipo_sanguineo,
                    'id_doador': doador.id_doador,
                    'pontuacao': doador.pontuacao,
                    'id_campanha': doador.id_campanha,
                }
                for pessoa, doador in resultados
            ]
        if tipo_perfil == 'Paciente':
            resultados = session.query(UsuarioPessoa, UsuarioPaciente).join(
                UsuarioPaciente, UsuarioPessoa.cpf == UsuarioPaciente.cpf
            ).all()
            return [
                {
                    'cpf': pessoa.cpf,
                    'nome_completo': pessoa.nome_completo,
                    'email': pessoa.email,
                    'cidade': pessoa.cidade,
                    'tipo_sanguineo': pessoa.tipo_sanguineo,
                    'id_paciente': paciente.id_paciente,
                    'data_entrada_fila': paciente.data_entrada_fila,
                    'id_instituicao': paciente.id_instituicao,
                }
                for pessoa, paciente in resultados
            ]
        resultados = session.query(UsuarioPessoa).all()
        return [_serialize_model(usuario) for usuario in resultados]
    finally:
        session.close()
