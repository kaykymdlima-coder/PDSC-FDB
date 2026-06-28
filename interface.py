import panel as pn
import pandas as pd
from datetime import date

from usuario import inserir_usuario, editar_usuario, remover_usuario, listar_usuarios

pn.extension(design='material')
# Botõess
u_cpf = pn.widgets.TextInput(name="CPF", placeholder="000.000.000-00", width=200)
u_nome = pn.widgets.TextInput(name="Nome Completo", width=300)
u_data_nasc = pn.widgets.DatePicker(name="Data de Nascimento", value=date(2000, 1, 1), width=200)
u_email = pn.widgets.TextInput(name="Email", width=250)
u_senha = pn.widgets.PasswordInput(name="Senha", width=200)
u_sexo = pn.widgets.Select(name="Sexo", options=["Masculino", "Feminino", "Outro"], width=150)
u_sangue = pn.widgets.Select(name="Tipo Sanguíneo", options=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], width=120)
u_logradouro = pn.widgets.TextInput(name="Logradouro", width=300)
u_bairro = pn.widgets.TextInput(name="Bairro", width=200)
u_cidade = pn.widgets.TextInput(name="Cidade", width=200)
u_cep = pn.widgets.TextInput(name="CEP", width=150)
u_tel = pn.widgets.TextInput(name="Telefone", width=150)

btn_inserir = pn.widgets.Button(name="Cadastrar", button_type="default", width=130)
btn_editar = pn.widgets.Button(name="Atualizar por CPF", button_type="default", width=140)
btn_remover = pn.widgets.Button(name="Remover por CPF", button_type="default", width=140)
btn_listar = pn.widgets.Button(name="Listar Usuários", button_type="default", width=140)

# Tabelas
tabela_usuarios = pn.widgets.Tabulator(pd.DataFrame(), width=900, height=250, visible=False)
titulo_lista = pn.pane.Markdown("## Usuários no Banco", visible=False)

# Funções de callback
def btn_inserir_click(event):
    dados = {
        "cpf": u_cpf.value,
        "nome_completo": u_nome.value,
        "data_nascimento": u_data_nasc.value,
        "email": u_email.value,
        "senha": u_senha.value,
        "sexo": u_sexo.value,
        "tipo_sanguineo": u_sangue.value,
        "logradouro": u_logradouro.value,
        "cidade": u_cidade.value,
        "bairro": u_bairro.value,
        "cep": u_cep.value,
        "telefone": u_tel.value
    }
    inserir_usuario(dados)
    tabela_usuarios.visible = False
    titulo_lista.visible = False

def btn_editar_click(event):
    dados = {
        "nome_completo": u_nome.value,
        "email": u_email.value,
        "cidade": u_cidade.value,
    }
    editar_usuario(u_cpf.value, dados)
    tabela_usuarios.visible = False
    titulo_lista.visible = False

def btn_remover_click(event):
    remover_usuario(u_cpf.value)
    tabela_usuarios.visible = False
    titulo_lista.visible = False

def btn_listar_click(event):
    # função pra fechar apos clicar dnv
    if tabela_usuarios.visible:
        tabela_usuarios.visible = False
        titulo_lista.visible = False
    else:
        lista = listar_usuarios()
        df = pd.DataFrame([{
            'CPF': u.cpf, 'Nome': u.nome_completo, 'Email': u.email, 
            'Cidade': u.cidade, 'Tipo Sanguíneo': u.tipo_sanguineo
        } for u in lista])
        
        tabela_usuarios.value = df
        tabela_usuarios.visible = True
        titulo_lista.visible = True

# Vincular os eventos aos botões
btn_inserir.on_click(btn_inserir_click)
btn_editar.on_click(btn_editar_click)
btn_remover.on_click(btn_remover_click)
btn_listar.on_click(btn_listar_click)

# Layoutzin clean
interface_usuario = pn.Column(
    "# Gerenciamento de Usuários (Pessoa)",
    pn.Row(u_cpf, u_nome, u_data_nasc),
    pn.Row(u_email, u_senha, u_sexo, u_sangue),
    pn.Row(u_logradouro, u_bairro, u_cidade, u_cep, u_tel),
    pn.Row(btn_inserir, btn_editar, btn_remover, btn_listar),
    pn.Spacer(height=15),
    titulo_lista,
    tabela_usuarios
)

interface_usuario.servable()