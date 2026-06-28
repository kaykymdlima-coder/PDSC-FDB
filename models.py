from datetime import date
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import Column, String, Date, Integer, ForeignKey, Numeric

Base = declarative_base()

class UsuarioPessoa(Base):
    __tablename__ = 'usuariopessoa'
    
    cpf = Column(String(14), primary_key=True, nullable=False)
    nome_completo = Column(String(150), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(64), nullable=False)
    sexo = Column(String(20), nullable=False)
    tipo_sanguineo = Column(String(5), nullable=False)
    logradouro = Column(String(150), nullable=False)
    cidade = Column(String(100), nullable=False)
    bairro = Column(String(100), nullable=False)
    cep = Column(String(10), nullable=False)
    telefone = Column(String(20), nullable=True)

class Instituicao(Base):
    __tablename__ = "instituicao"
    id_instituicao = Column(Integer, primary_key=True, nullable=False)
    cnpj = Column(String(18), nullable=False, unique=True)
    nome = Column(String(150), nullable=False)
    registro_cnes = Column(String(50), nullable=False, unique=True)
    telefone_institucional = Column(String(20), nullable=False, unique=True)
    email_institucional = Column(String(100), nullable=False, unique=True)
    senha = Column(String(64), nullable=False)
    cep = Column(String(10), nullable=False)
    logradouro = Column(String(150), nullable=False)
    cidade = Column(String(100), nullable=False)
    bairro = Column(String(100), nullable=False)

class Campanha(Base):
    __tablename__ = "campanhas"
    id_campanha = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String(150), nullable=False)
    regiao = Column(String(100), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    redes_sociais = Column(String(150), nullable=True)
    id_instituicao = Column(Integer, ForeignKey("instituicao.id_instituicao"), nullable=False)

# --- NOVAS ENTIDADES DERIVADAS DE PESSOA ---

class UsuarioDoador(Base):
    __tablename__ = 'usuariodoador'
    id_doador = Column(Integer, primary_key=True, nullable=False)
    cpf = Column(String(14), ForeignKey('usuariopessoa.cpf'), primary_key=True, nullable=False)
    pontuacao = Column(Integer, nullable=False, default=0)
    id_campanha = Column(Integer, ForeignKey('campanhas.id_campanha'), nullable=False)

class UsuarioPaciente(Base):
    __tablename__ = 'usuariopaciente'
    id_paciente = Column(Integer, primary_key=True, nullable=False)
    cpf = Column(String(14), ForeignKey('usuariopessoa.cpf'), primary_key=True, nullable=False)
    data_entrada_fila = Column(Date, nullable=False)
    id_instituicao = Column(Integer, ForeignKey('instituicao.id_instituicao'), nullable=False)