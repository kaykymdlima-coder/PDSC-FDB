from conexao import Session
from models import Instituicao, Campanha
from datetime import date

def popular():
    with Session() as session:
        try:
            # 1. Verifica e insere a instituicao com ID 1
            inst = session.query(Instituicao).filter_by(id_instituicao=1).first()
            if not inst:
                nova_inst = Instituicao(
                    id_instituicao=1, 
                    cnpj="00.000.000/0001-00", 
                    nome="Hospital Central de Testes",
                    registro_cnes="12345", 
                    telefone_institucional="1122223333",
                    email_institucional="hospital@teste.com", 
                    senha="123",
                    cep="00000-000", 
                    logradouro="Rua da Saúde, 123", 
                    cidade="Quixadá", 
                    bairro="Centro"
                )
                session.add(nova_inst)
                session.flush()

            # 2. Verifica e insere a campanha vinculada à instituicao 1
            camp = session.query(Campanha).filter_by(id_campanha=1).first()
            if not camp:
                nova_camp = Campanha(
                    id_campanha=1, 
                    nome="Campanha Geral de Doação", 
                    regiao="Geral",
                    data_inicio=date.today(), 
                    data_fim=date.today(), 
                    status="Ativa",
                    id_instituicao=1
                )
                session.add(nova_camp)

            session.commit()
            print("Sucesso: Dados iniciais inseridos no banco de dados.")
        except Exception as e:
            session.rollback()
            print(f"Erro: Falha ao inserir dados no banco. Detalhes: {e}")

if __name__ == "__main__":
    popular()