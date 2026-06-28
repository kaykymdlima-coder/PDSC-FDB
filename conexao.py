from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Onde guarda os dados da conexao
USUARIO = "postgres"
SENHA = "raisondettre"
HOST = "localhost"
PORTA = "5432"
BANCO = "PDSC"

#string de conexão
DATABASE_URL = (
    f"postgresql+psycopg2://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"
)

#engine q ria a conexão
engine = create_engine(DATABASE_URL)

#novo execute
Session = sessionmaker(bind=engine)