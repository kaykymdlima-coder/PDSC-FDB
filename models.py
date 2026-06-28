from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Date, Integer

Base = declarative_base()

class UsuarioPessoa(Base):
    __tablename__ = 'usuariopessoa'
    
    nome_completo = Column(String(150), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    cpf = Column(String(14), primary_key=True, nullable=False)
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
    id_instituicao: Mapped[int] = mapped_column(Integer, primary_key=True)
    cnpj: Mapped[str] = mapped_column(String(18), unique=True)
    nome: Mapped[str] = mapped_column(String(150))
    registro_cnes: Mapped[str] = mapped_column(String(50), unique=True)
    telefone_institucional: Mapped[str] = mapped_column(String(20), unique=True)
    email_institucional: Mapped[str] = mapped_column(String(100), unique=True)
    senha: Mapped[str] = mapped_column(String(64))
    cep: Mapped[str] = mapped_column(String(10))
    logradouro: Mapped[str] = mapped_column(String(150))
    cidade: Mapped[str] = mapped_column(String(100))
    bairro: Mapped[str] = mapped_column(String(100))
    campanhas: Mapped[list["Campanha"]] = relationship(back_populates="instituicao")


class Campanha(Base):
    __tablename__ = "campanhas"
    id_campanha: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(150))
    regiao: Mapped[str] = mapped_column(String(100))
    data_inicio: Mapped[date] = mapped_column(Date)
    data_fim: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50))
    redes_sociais: Mapped[str | None] = mapped_column(String(150), nullable=True)
    id_instituicao: Mapped[int] = mapped_column(ForeignKey("instituicao.id_instituicao"))

    instituicao: Mapped["Instituicao"] = relationship(back_populates="campanhas")