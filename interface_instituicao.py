import pandas as pd
import panel as pn
from crud_instituicao import (
    listar_instituicoes,
    adicionar_instituicao,
    editar_instituicao,
    excluir_instituicao,
    obter_instituicao_por_id,
)

pn.extension()

# ---------- Tabela ----------
table = pn.widgets.Tabulator(
    value=pd.DataFrame(listar_instituicoes()),
    pagination='remote',
    page_size=10,
    selectable=True,
    show_index=False,
    widths={
        'id_instituicao': 80,
        'cnpj': 120,
        'nome': 180,
        'registro_cnes': 120,
        'telefone_institucional': 130,
        'email_institucional': 180,
        'senha': 100,
        'cep': 100,
        'logradouro': 180,
        'cidade': 120,
        'bairro': 120,
    },
)

# ---------- Formulário ----------
id_instituicao_input = pn.widgets.IntInput(name='ID Instituição', placeholder='Digite o ID')
cnpj_input = pn.widgets.TextInput(name='CNPJ', placeholder='Ex: 12.345.678/0001-99')
nome_input = pn.widgets.TextInput(name='Nome', placeholder='Nome da instituição')
registro_cnes_input = pn.widgets.TextInput(name='Registro CNES', placeholder='Número do CNES')
telefone_input = pn.widgets.TextInput(name='Telefone', placeholder='(11) 99999-9999')
email_input = pn.widgets.TextInput(name='E-mail', placeholder='instituicao@email.com')
senha_input = pn.widgets.PasswordInput(name='Senha', placeholder='Senha de acesso')
cep_input = pn.widgets.TextInput(name='CEP', placeholder='01001-000')
logradouro_input = pn.widgets.TextInput(name='Logradouro', placeholder='Rua, Avenida...')
cidade_input = pn.widgets.TextInput(name='Cidade', placeholder='Cidade')
bairro_input = pn.widgets.TextInput(name='Bairro', placeholder='Bairro')

# Botões
btn_add = pn.widgets.Button(name='Adicionar', button_type='success')
btn_edit = pn.widgets.Button(name='Editar', button_type='primary')
btn_delete = pn.widgets.Button(name='Excluir', button_type='danger')
btn_refresh = pn.widgets.Button(name='Atualizar', button_type='default')

status_msg = pn.pane.Markdown('', styles={'color': 'green'})

# ---------- Funções auxiliares ----------
def refresh_all():
    """Atualiza a tabela com os dados mais recentes."""
    table.value = pd.DataFrame(listar_instituicoes())
    status_msg.object = 'Dados atualizados.'
    status_msg.styles = {'color': 'green'}

def clear_form():
    id_instituicao_input.value = None
    cnpj_input.value = ''
    nome_input.value = ''
    registro_cnes_input.value = ''
    telefone_input.value = ''
    email_input.value = ''
    senha_input.value = ''
    cep_input.value = ''
    logradouro_input.value = ''
    cidade_input.value = ''
    bairro_input.value = ''

def get_form_data() -> dict:
    return {
        'id_instituicao': id_instituicao_input.value,
        'cnpj': cnpj_input.value,
        'nome': nome_input.value,
        'registro_cnes': registro_cnes_input.value,
        'telefone_institucional': telefone_input.value,
        'email_institucional': email_input.value,
        'senha': senha_input.value,
        'cep': cep_input.value,
        'logradouro': logradouro_input.value,
        'cidade': cidade_input.value,
        'bairro': bairro_input.value,
    }

def is_form_valid() -> bool:
    dados = get_form_data()
    return all([
        dados['id_instituicao'] is not None,
        dados['cnpj'],
        dados['nome'],
        dados['registro_cnes'],
        dados['telefone_institucional'],
        dados['email_institucional'],
        dados['senha'],
        dados['cep'],
        dados['logradouro'],
        dados['cidade'],
        dados['bairro'],
    ])

# ---------- Callbacks ----------
def on_add(event):
    if not is_form_valid():
        status_msg.object = 'Preencha todos os campos obrigatórios.'
        status_msg.styles = {'color': 'red'}
        return
    dados = get_form_data()
    sucesso = adicionar_instituicao(dados)
    if sucesso:
        status_msg.object = f'Instituição {dados["id_instituicao"]} adicionada!'
        status_msg.styles = {'color': 'green'}
        clear_form()
        refresh_all()
    else:
        status_msg.object = 'Erro ao adicionar. Verifique se o ID ou CNES/CNPJ já existem.'
        status_msg.styles = {'color': 'red'}

def on_edit(event):
    row = table.selection
    if row is None or row.empty:
        status_msg.object = 'Selecione uma instituição para editar.'
        status_msg.styles = {'color': 'red'}
        return
    if not is_form_valid():
        status_msg.object = 'Preencha todos os campos obrigatórios.'
        status_msg.styles = {'color': 'red'}
        return
    dados = get_form_data()
    # Remove ID do dicionário para não tentar alterar a chave primária
    dados_edit = {k: v for k, v in dados.items() if k != 'id_instituicao'}
    sucesso = editar_instituicao(dados['id_instituicao'], dados_edit)
    if sucesso:
        status_msg.object = f'Instituição {dados["id_instituicao"]} atualizada!'
        status_msg.styles = {'color': 'green'}
        clear_form()
        refresh_all()
    else:
        status_msg.object = 'Erro ao editar. Verifique os dados.'
        status_msg.styles = {'color': 'red'}

def on_delete(event):
    row = table.selection
    if row is None or row.empty:
        status_msg.object = 'Selecione uma instituição para excluir.'
        status_msg.styles = {'color': 'red'}
        return
    selected_id = row.iloc[0]['id_instituicao']
    sucesso = excluir_instituicao(selected_id)
    if sucesso:
        status_msg.object = f'Instituição {selected_id} excluída.'
        status_msg.styles = {'color': 'green'}
        clear_form()
        refresh_all()
    else:
        status_msg.object = 'Erro ao excluir. Verifique se há campanhas vinculadas.'
        status_msg.styles = {'color': 'red'}

def on_table_select(event):
    row = table.selection
    if row is not None and not row.empty:
        data = row.iloc[0]
        id_instituicao_input.value = data['id_instituicao']
        cnpj_input.value = data['cnpj']
        nome_input.value = data['nome']
        registro_cnes_input.value = data['registro_cnes']
        telefone_input.value = data['telefone_institucional']
        email_input.value = data['email_institucional']
        senha_input.value = data['senha']
        cep_input.value = data['cep']
        logradouro_input.value = data['logradouro']
        cidade_input.value = data['cidade']
        bairro_input.value = data['bairro']

def on_refresh(event):
    refresh_all()

# Conecta eventos
btn_add.on_click(on_add)
btn_edit.on_click(on_edit)
btn_delete.on_click(on_delete)
btn_refresh.on_click(on_refresh)
table.on_click(on_table_select)

# ---------- Layout ----------
form = pn.Column(
    pn.Row(id_instituicao_input, cnpj_input),
    pn.Row(nome_input, registro_cnes_input),
    pn.Row(telefone_input, email_input),
    pn.Row(senha_input, cep_input),
    pn.Row(logradouro_input, cidade_input),
    pn.Row(bairro_input),
    pn.Row(btn_add, btn_edit, btn_delete, btn_refresh),
    status_msg,
)

dashboard = pn.Row(
    pn.Column(table, sizing_mode='stretch_width'),
    pn.Column(form, width=450)
)

# Para servir:
if __name__ == "__main__":
    pn.serve(dashboard, address="0.0.0.0", port=8889, show=False)