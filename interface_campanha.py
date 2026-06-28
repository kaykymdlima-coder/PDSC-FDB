import pandas as pd
import panel as pn
from campanhas import (
    listar_campanhas,
    listar_instituicoes,
    adicionar_campanha,
    editar_campanha,
    excluir_campanha,
    obter_campanha_por_id,
)
from datetime import date

pn.extension()  

table = pn.widgets.Tabulator(
    value=pd.DataFrame(listar_campanhas()),
    pagination='remote',
    page_size=10,
    selectable=True,
    show_index=False,
    widths={
        'id_campanha': 80,
        'nome': 150,
        'regiao': 120,
        'data_inicio': 100,
        'data_fim': 100,
        'status': 100,
        'redes_sociais': 150,
        'id_instituicao': 100,
    },
)

id_campanha_input = pn.widgets.IntInput(name='ID Campanha', placeholder='Digite o ID')
nome_input = pn.widgets.TextInput(name='Nome', placeholder='Nome da campanha')
regiao_input = pn.widgets.TextInput(name='Região', placeholder='Região')
data_inicio = pn.widgets.DatePicker(name='Data Início')
data_fim = pn.widgets.DatePicker(name='Data Fim')
status_input = pn.widgets.TextInput(name='Status', placeholder='Ex: Ativa, Encerrada')
redes_sociais_input = pn.widgets.TextInput(name='Redes Sociais', placeholder='URLs ou descrição')

instituicoes_opts = {i['id']: i['nome'] for i in listar_instituicoes()}
instituicao_dropdown = pn.widgets.Select(
    name='Instituição',
    options=instituicoes_opts,
)

btn_add = pn.widgets.Button(name='Adicionar', button_type='success')
btn_edit = pn.widgets.Button(name='Editar', button_type='primary')
btn_delete = pn.widgets.Button(name='Excluir', button_type='danger')
btn_refresh = pn.widgets.Button(name='Atualizar', button_type='default')

status_msg = pn.pane.Markdown('', styles={'color': 'green'})


def refresh_all():
    """Atualiza a tabela e o dropdown de instituições."""
    table.value = pd.DataFrame(listar_campanhas())
    novas_opts = {i['id']: i['nome'] for i in listar_instituicoes()}
    instituicao_dropdown.options = novas_opts
    status_msg.object = 'Dados atualizados.'

def clear_form():
    id_campanha_input.value = None
    nome_input.value = ''
    regiao_input.value = ''
    data_inicio.value = None
    data_fim.value = None
    status_input.value = ''
    redes_sociais_input.value = ''
    instituicao_dropdown.value = next(iter(instituicao_dropdown.options)) if instituicao_dropdown.options else None

def get_form_data() -> dict:
    return {
        'id_campanha': id_campanha_input.value,
        'nome': nome_input.value,
        'regiao': regiao_input.value,
        'data_inicio': data_inicio.value,
        'data_fim': data_fim.value,
        'status': status_input.value,
        'redes_sociais': redes_sociais_input.value if redes_sociais_input.value else None,
        'id_instituicao': instituicao_dropdown.value,
    }

def is_form_valid() -> bool:
    dados = get_form_data()
    return all([
        dados['id_campanha'] is not None,
        dados['nome'],
        dados['regiao'],
        dados['data_inicio'] is not None,
        dados['data_fim'] is not None,
        dados['status'],
        dados['id_instituicao'] is not None,
    ])

def on_add(event):
    if not is_form_valid():
        status_msg.object = 'Preencha todos os campos obrigatórios.'
        status_msg.styles = {'color': 'red'}
        return
    dados = get_form_data()
    sucesso = adicionar_campanha(dados)
    if sucesso:
        status_msg.object = f'Campanha {dados["id_campanha"]} adicionada!'
        status_msg.styles = {'color': 'green'}
        clear_form()
        refresh_all()
    else:
        status_msg.object = 'Erro ao adicionar. Verifique se o ID já existe.'
        status_msg.styles = {'color': 'red'}

def on_edit(event):
    row = table.selection
    if row is None or row.empty:
        status_msg.object = 'Selecione uma campanha para editar.'
        status_msg.styles = {'color': 'red'}
        return
    if not is_form_valid():
        status_msg.object = 'Preencha todos os campos obrigatórios.'
        status_msg.styles = {'color': 'red'}
        return
    dados = get_form_data()
    dados_edit = {k: v for k, v in dados.items() if k != 'id_campanha'}
    sucesso = editar_campanha(dados['id_campanha'], dados_edit)
    if sucesso:
        status_msg.object = f'Campanha {dados["id_campanha"]} atualizada!'
        status_msg.styles = {'color': 'green'}
        clear_form()
        refresh_all()
    else:
        status_msg.object = 'Erro ao editar. Verifique os dados.'
        status_msg.styles = {'color': 'red'}

def on_delete(event):
    row = table.selection
    if row is None or row.empty:
        status_msg.object = 'Selecione uma campanha para excluir.'
        status_msg.styles = {'color': 'red'}
        return
    selected_id = row.iloc[0]['id_campanha']
    sucesso = excluir_campanha(selected_id)
    if sucesso:
        status_msg.object = f'Campanha {selected_id} excluída.'
        status_msg.styles = {'color': 'green'}
        clear_form()
        refresh_all()
    else:
        status_msg.object = 'Erro ao excluir. Verifique se há dependências.'
        status_msg.styles = {'color': 'red'}

def on_table_select(event):
    row = table.selection
    if row is not None and not row.empty:
        data = row.iloc[0]
        id_campanha_input.value = data['id_campanha']
        nome_input.value = data['nome']
        regiao_input.value = data['regiao']
        data_inicio.value = data['data_inicio']
        data_fim.value = data['data_fim']
        status_input.value = data['status']
        redes_sociais_input.value = data['redes_sociais'] if pd.notna(data['redes_sociais']) else ''
        if data['id_instituicao'] in instituicao_dropdown.options:
            instituicao_dropdown.value = data['id_instituicao']

def on_refresh(event):
    refresh_all()

btn_add.on_click(on_add)
btn_edit.on_click(on_edit)
btn_delete.on_click(on_delete)
btn_refresh.on_click(on_refresh)
table.on_click(on_table_select)

form = pn.Column(
    pn.Row(id_campanha_input, nome_input),
    pn.Row(regiao_input, instituicao_dropdown),
    pn.Row(data_inicio, data_fim),
    pn.Row(status_input, redes_sociais_input),
    pn.Row(btn_add, btn_edit, btn_delete, btn_refresh),
    status_msg,
)

dashboard = pn.Row(
    pn.Column(table, sizing_mode='stretch_width'),
    pn.Column(form, width=400)
)