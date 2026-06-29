import pandas as pd
import panel as pn
from datetime import date
import time

from usuario import inserir_usuario, editar_usuario, remover_usuario, listar_usuarios
from campanhas import listar_campanhas

pn.extension(design='material')

select_perfil = pn.widgets.Select(
    name='Perfil do Usuário',
    options=['Pessoa Comum', 'Doador', 'Paciente'],
    width=260,
)

u_cpf = pn.widgets.TextInput(name='CPF', placeholder='000.000.000-00', width=200)
row_nome = pn.widgets.TextInput(name='Nome Completo', width=360)
row_data_nasc = pn.widgets.DatePicker(name='Data de Nascimento', value=date(2000, 1, 1), width=220)
row_email = pn.widgets.TextInput(name='Email', width=320)
row_senha = pn.widgets.PasswordInput(name='Senha', width=220)
row_sexo = pn.widgets.Select(name='Sexo', options=['Masculino', 'Feminino', 'Outro'], width=180)
row_sangue = pn.widgets.Select(name='Tipo Sanguíneo', options=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], width=180)
row_logradouro = pn.widgets.TextInput(name='Logradouro', width=360)
row_bairro = pn.widgets.TextInput(name='Bairro', width=220)
row_cidade = pn.widgets.TextInput(name='Cidade', width=220)
row_cep = pn.widgets.TextInput(name='CEP', width=160)
row_tel = pn.widgets.TextInput(name='Telefone', width=200)

d_pontos = pn.widgets.IntInput(name='Pontuação Inicial', value=0, width=180, visible=False)
# carregar campanhas existentes e disponibilizar em Select para evitar FK inválida
_campanhas = listar_campanhas()
_camp_options = {f"{c['id_campanha']} - {c['nome']}": c['id_campanha'] for c in _campanhas}
_camp_default = next(iter(_camp_options.values()), None)
d_campanha = pn.widgets.Select(name='Campanha', options=_camp_options, value=_camp_default, width=220, visible=False)

p_fila = pn.widgets.DatePicker(name='Data Entrada na Fila', value=date.today(), width=220, visible=False)
p_instituicao = pn.widgets.IntInput(name='ID da Instituição', value=1, width=220, visible=False)

campos_extras = pn.Row(visible=False)

btn_inserir = pn.widgets.Button(name='Cadastrar', button_type='default', width=140)
btn_editar = pn.widgets.Button(name='Atualizar', button_type='default', width=160)
btn_remover = pn.widgets.Button(name='Remover', button_type='default', width=160)
btn_listar = pn.widgets.Button(name='Listar Usuários', button_type='default', width=160)

status_msg = pn.pane.Markdown('', styles={'font-weight': 'bold'})

tabela_usuarios = pn.widgets.Tabulator(pd.DataFrame(), width=520, height=280, visible=False)
titulo_lista = pn.pane.Markdown('## Resultado da Pesquisa', visible=False)


def atualizar_campos_perfil(event):
    perfil = event.new
    if perfil == 'Doador':
        d_pontos.visible = d_campanha.visible = True
        p_fila.visible = p_instituicao.visible = False
        campos_extras.objects = [d_pontos, d_campanha]
        campos_extras.visible = True
    elif perfil == 'Paciente':
        d_pontos.visible = d_campanha.visible = False
        p_fila.visible = p_instituicao.visible = True
        campos_extras.objects = [p_fila, p_instituicao]
        campos_extras.visible = True
    else:
        campos_extras.visible = False
        campos_extras.objects = []

select_perfil.param.watch(atualizar_campos_perfil, 'value')


def obter_dados_pessoa():
    return {
        'cpf': u_cpf.value.strip(),
        'nome_completo': row_nome.value.strip(),
        'data_nascimento': row_data_nasc.value,
        'email': row_email.value.strip(),
        'senha': row_senha.value,
        'sexo': row_sexo.value,
        'tipo_sanguineo': row_sangue.value,
        'logradouro': row_logradouro.value.strip(),
        'cidade': row_cidade.value.strip(),
        'bairro': row_bairro.value.strip(),
        'cep': row_cep.value.strip(),
        'telefone': row_tel.value.strip(),
    }


def campos_validos():
    dados = obter_dados_pessoa()
    obrigatorios = [
        dados['cpf'],
        dados['nome_completo'],
        dados['data_nascimento'],
        dados['email'],
        dados['senha'],
        dados['sexo'],
        dados['tipo_sanguineo'],
        dados['logradouro'],
        dados['cidade'],
        dados['bairro'],
        dados['cep'],
    ]
    return all(obrigatorios)


def limpar_formulario():
    u_cpf.value = ''
    row_nome.value = ''
    row_data_nasc.value = date(2000, 1, 1)
    row_email.value = ''
    row_senha.value = ''
    row_sexo.value = 'Masculino'
    row_sangue.value = 'A+'
    row_logradouro.value = ''
    row_bairro.value = ''
    row_cidade.value = ''
    row_cep.value = ''
    row_tel.value = ''
    d_pontos.value = 0
    d_campanha.value = 1
    p_fila.value = date.today()
    p_instituicao.value = 1
    titulo_lista.visible = False
    tabela_usuarios.visible = False
    results_card.visible = False


def atualizar_tabela():
    perfil = select_perfil.value
    lista = listar_usuarios(tipo_perfil=perfil)
    registros = []

    for item in lista:
        if perfil == 'Doador':
            registros.append({
                'ID Doador': item.get('id_doador'),
                'CPF': item.get('cpf'),
                'Nome': item.get('nome_completo'),
                'Pontos': item.get('pontuacao'),
                'ID Campanha': item.get('id_campanha'),
            })
        elif perfil == 'Paciente':
            registros.append({
                'ID Paciente': item.get('id_paciente'),
                'CPF': item.get('cpf'),
                'Nome': item.get('nome_completo'),
                'Fila Desde': item.get('data_entrada_fila'),
                'ID Instituição': item.get('id_instituicao'),
            })
        else:
            registros.append({
                'CPF': item.get('cpf'),
                'Nome': item.get('nome_completo'),
                'Email': item.get('email'),
                'Cidade': item.get('cidade'),
                'Tipo Sanguíneo': item.get('tipo_sanguineo'),
            })

    tabela_usuarios.value = pd.DataFrame(registros)
    tem_registros = len(registros) > 0
    tabela_usuarios.visible = tem_registros
    titulo_lista.visible = tem_registros
    return tem_registros


def atualizar_status(texto, sucesso=True):
    status_msg.object = texto


def btn_inserir_click(event):
    if not campos_validos():
        atualizar_status('Preencha todos os campos obrigatórios.', sucesso=False)
        return

    dados = obter_dados_pessoa()
    perfil = select_perfil.value
    dados_extras = None

    if perfil == 'Doador':
        dados_extras = {
            'id_doador': int(time.time()) & 0xfffffff,
            'pontuacao': d_pontos.value,
            'id_campanha': d_campanha.value,
        }
    elif perfil == 'Paciente':
        dados_extras = {
            'id_paciente': int(time.time()) & 0xfffffff,
            'data_entrada_fila': p_fila.value,
            'id_instituicao': p_instituicao.value,
        }

    sucesso = inserir_usuario(dados, tipo_perfil=perfil, dados_extras=dados_extras)
    if sucesso:
        atualizar_status('Usuário cadastrado com sucesso.')
        limpar_formulario()
    else:
        atualizar_status('Falha ao cadastrar o usuário. Verifique os dados e tente novamente.', sucesso=False)


def btn_editar_click(event):
    if not u_cpf.value.strip():
        atualizar_status('Informe o CPF para atualizar o usuário.', sucesso=False)
        return

    dados = {
        'nome_completo': row_nome.value.strip(),
        'email': row_email.value.strip(),
        'cidade': row_cidade.value.strip(),
    }
    sucesso = editar_usuario(u_cpf.value.strip(), dados)
    if sucesso:
        atualizar_status('Usuário atualizado com sucesso.')
        limpar_formulario()
    else:
        atualizar_status('Falha ao atualizar. Verifique se o CPF existe.', sucesso=False)


def btn_remover_click(event):
    if not u_cpf.value.strip():
        atualizar_status('Informe o CPF para remover o usuário.', sucesso=False)
        return

    sucesso = remover_usuario(u_cpf.value.strip())
    if sucesso:
        atualizar_status('Usuário removido com sucesso.')
        limpar_formulario()
    else:
        atualizar_status('Falha ao remover. Verifique se o CPF existe.', sucesso=False)


def btn_listar_click(event):
    if results_card.visible:
        results_card.visible = False
        tabela_usuarios.visible = False
        titulo_lista.visible = False
        atualizar_status('Tabela oculta.')
        return

    tem_registros = atualizar_tabela()
    if tem_registros:
        results_card.visible = True
        atualizar_status('Tabela exibida.')
    else:
        results_card.visible = False
        atualizar_status('Nenhum usuário encontrado para o perfil selecionado.', sucesso=False)


btn_inserir.on_click(btn_inserir_click)
btn_editar.on_click(btn_editar_click)
btn_remover.on_click(btn_remover_click)
btn_listar.on_click(btn_listar_click)

form_card = pn.Card(
    pn.pane.Markdown('## Formulário de Usuários'),
    select_perfil,
    pn.Row(u_cpf, row_nome, row_data_nasc),
    pn.Row(row_email, row_senha, row_sexo, row_sangue),
    pn.Row(row_logradouro, row_bairro, row_cidade, row_cep, row_tel),
    campos_extras,
    pn.Row(btn_inserir, btn_editar, btn_remover, btn_listar),
    status_msg,
    sizing_mode='stretch_width',
    width=520,
    margin=(0, 0, 0, 0),
)

results_card = pn.Card(
    titulo_lista,
    tabela_usuarios,
    title='Resultado da Pesquisa',
    sizing_mode='stretch_width',
    width=520,
    margin=(0, 0, 0, 0),
    visible=False,
)

interface_usuario = pn.Column(
    pn.pane.Markdown('# Gerenciamento de Usuários'),
    pn.Spacer(height=12),
    form_card,
    results_card,
)

interface_usuario.servable(title='Usuários')
