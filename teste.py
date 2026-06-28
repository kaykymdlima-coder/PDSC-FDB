import psycopg2

try:
    conexao = psycopg2.connect(
        host="localhost",
        database="PDSC",
        user="postgres",
        password="raisondettre",
        port="5432"
    )

    print("Conectado com sucesso!")

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome_completo, cpf, email
        FROM usuariopessoa;
    """)

    pessoas = cursor.fetchall()

    print(pessoas)

    cursor.close()
    conexao.close()

except Exception as erro:
    print("Erro:", erro)