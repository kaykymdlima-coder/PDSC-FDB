from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Date

class Base(DeclarativeBase):
    pass


class UsuarioPessoa(Base):
    tablename = "usuariopessoa"

    cpf: Mapped[str] = mapped_column(String(14), primary_key=True)
    nome_completo: Mapped[str] = mapped_column(String(150))
    data_nascimento: Mapped[Date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    senha: Mapped[str] = mapped_column(String(64))
    sexo: Mapped[str] = mapped_column(String(20))
    tipo_sanguineo: Mapped[str] = mapped_column(String(5))
    logradouro: Mapped[str] = mapped_column(String(150))
    cidade: Mapped[str] = mapped_column(String(100))
    bairro: Mapped[str] = mapped_column(String(100))
    cep: Mapped[str] = mapped_column(String(10))
    telefone: Mapped[str] = mapped_column(String(20), nullable=True)



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