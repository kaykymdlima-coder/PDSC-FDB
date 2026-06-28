import panel as pn
import pandas as pd
from datetime import date

from usuario import inserir_usuario, editar_usuario, remover_usuario, listar_usuarios

pn.extension(design='material')

# --- SELETOR DE PERFIL ---
select_perfil = pn.widgets.Select(name="Perfil do Usuário", options=["Pessoa Comum", "Doador", "Paciente"], width=220)

# --- WIDGETS GERAIS (PESSOA) ---
u_cpf = pn.widgets.TextInput(name="CPF", placeholder="000.000.000-00", width=180)
u_nome = pn.widgets.TextInput(name="Nome Completo", width=350)
u_data_nasc = pn.widgets.DatePicker(name="Data de Nascimento", value=date(2000, 1, 1), width=200)
u_email = pn.widgets.TextInput(name="Email", width=280)
u_senha = pn.widgets.PasswordInput(name="Senha", width=180)
u_sexo = pn.widgets.Select(name="Sexo", options=["Masculino", "Feminino", "Outro"], width=160)
u_sangue = pn.widgets.Select(name="Tipo Sanguíneo", options=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], width=160)
u_logradouro = pn.widgets.TextInput(name="Logradouro", width=350)
u_bairro = pn.widgets.TextInput(name="Bairro", width=200)
u_cidade = pn.widgets.TextInput(name="Cidade", width=200)
u_cep = pn.widgets.TextInput(name="CEP", width=140)
u_tel = pn.widgets.TextInput(name="Telefone", width=160)

# --- WIDGETS ESPECÍFICOS (SEM OS IDS SEQUENCIAIS NA TELA) ---
d_pontos = pn.widgets.IntInput(name="Pontuação Inicial", value=0, width=160, visible=False)
d_campanha = pn.widgets.IntInput(name="ID da Campanha (Obrigatório)", value=1, width=260, visible=False)

p_fila = pn.widgets.DatePicker(name="Data Entrada na Fila", value=date.today(), width=200, visible=False)
p_instituicao = pn.widgets.IntInput(name="ID da Instituição (Obrigatório)", value=1, width=260, visible=False)

# Container para os campos dinâmicos
campos_extras = pn.Row(visible=False)

# --- BOTÕES ---
btn_inserir = pn.widgets.Button(name="Cadastrar", button_type="default", width=130)
btn_editar = pn.widgets.Button(name="Atualizar por CPF", button_type="default", width=140)
btn_remover = pn.widgets.Button(name="Remover por CPF", button_type="default", width=140)
btn_listar = pn.widgets.Button(name="Listar Usuários", button_type="default", width=140)

tabela_usuarios = pn.widgets.Tabulator(pd.DataFrame(), width=950, height=250, visible=False)
titulo_lista = pn.pane.Markdown("## Dados Filtrados", visible=False)

# --- CALLBACK PARA MUDANÇA DE PERFIL ---
def atualizar_campos_perfil(event):
    perfil = event.new
    if perfil == "Doador":
        d_pontos.visible = d_campanha.visible = True
        p_fila.visible = p_instituicao.visible = False
        campos_extras.objects = [d_pontos, d_campanha]
        campos_extras.visible = True
    elif perfil == "Paciente":
        d_pontos.visible = d_campanha.visible = False
        p_fila.visible = p_instituicao.visible = True
        campos_extras.objects = [p_fila, p_instituicao]
        campos_extras.visible = True
    else:
        campos_extras.visible = False
        campos_extras.objects = []

select_perfil.param.watch(atualizar_campos_perfil, 'value')

# --- CALLBACKS DOS BOTÕES ---
def btn_inserir_click(event):
    dados = {
        "cpf": u_cpf.value, "nome_completo": u_nome.value, "data_nascimento": u_data_nasc.value,
        "email": u_email.value, "senha": u_senha.value, "sexo": u_sexo.value, "tipo_sanguineo": u_sangue.value,
        "logradouro": u_logradouro.value, "cidade": u_cidade.value, "bairro": u_bairro.value,
        "cep": u_cep.value, "telefone": u_tel.value
    }
    
    dados_extras = None
    perfil = select_perfil.value
    if perfil == "Doador":
        dados_extras = {"pontuacao": d_pontos.value, "id_campanha": d_campanha.value}
    elif perfil == "Paciente":
        dados_extras = {"data_entrada_fila": p_fila.value, "id_instituicao": p_instituicao.value}
        
    inserir_usuario(dados, tipo_perfil=perfil, dados_extras=dados_extras)
    tabela_usuarios.visible = False
    titulo_lista.visible = False

def btn_editar_click(event):
    dados = {"nome_completo": u_nome.value, "email": u_email.value, "cidade": u_cidade.value}
    editar_usuario(u_cpf.value, dados)
    tabela_usuarios.visible = False
    titulo_lista.visible = False

def btn_remover_click(event):
    remover_usuario(u_cpf.value)
    tabela_usuarios.visible = False
    titulo_lista.visible = False

def btn_listar_click(event):
    if tabela_usuarios.visible:
        tabela_usuarios.visible = False
        titulo_lista.visible = False
    else:
        perfil = select_perfil.value
        lista = listar_usuarios(tipo_perfil=perfil)
        
        registros = []
        if perfil == "Doador":
            for p, d in lista:
                registros.append({'ID Doador': d.id_doador, 'CPF': p.cpf, 'Nome': p.nome_completo, 'Pontos': d.pontuacao, 'ID Campanha': d.id_campanha})
        elif perfil == "Paciente":
            for p, pac in lista:
                registros.append({'ID Paciente': pac.id_paciente, 'CPF': p.cpf, 'Nome': p.nome_completo, 'Fila Desde': pac.data_entrada_fila, 'ID Inst.': pac.id_instituicao})
        else:
            for p in lista:
                registros.append({'CPF': p.cpf, 'Nome': p.nome_completo, 'Email': p.email, 'Cidade': p.cidade, 'Sangue': p.tipo_sanguineo})
                
        tabela_usuarios.value = pd.DataFrame(registros)
        tabela_usuarios.visible = True
        titulo_lista.visible = True

btn_inserir.on_click(btn_inserir_click)
btn_editar.on_click(btn_editar_click)
btn_remover.on_click(btn_remover_click)
btn_listar.on_click(btn_listar_click)

# --- LAYOUT ---
interface_usuario = pn.Column(
    "# Gerenciamento de Usuários (Pessoa / Doador / Paciente)",
    select_perfil,
    pn.Row(u_cpf, u_nome, u_data_nasc),
    pn.Row(u_email, u_senha, u_sexo, u_sangue),
    pn.Row(u_logradouro, u_bairro, u_cidade, u_cep, u_tel),
    campos_extras,
    pn.Spacer(height=10),
    pn.Row(btn_inserir, btn_editar, btn_remover, btn_listar),
    pn.Spacer(height=15),
    titulo_lista,
    tabela_usuarios
)

interface_usuario.servable()