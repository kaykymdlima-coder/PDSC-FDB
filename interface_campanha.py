import pandas as pd
import panel as pn
from campanhas import (
    listar_campanhas,
    listar_instituicoes,
    adicionar_campanha,
    editar_campanha,
    excluir_campanha,
)
from datetime import date

pn.extension(design='material')


def carregar_opcoes_instituicoes():
    instituicoes = listar_instituicoes()
    if not instituicoes:
        return {"Nenhuma instituição cadastrada": 0}
    return {item["nome"]: item["id"] for item in instituicoes}


def construir_dataframe(campanhas):
    if campanhas:
        return pd.DataFrame(campanhas)
    return pd.DataFrame(columns=[
        'id_campanha', 'nome', 'regiao', 'data_inicio', 'data_fim', 'status', 'redes_sociais', 'id_instituicao'
    ])

campanhas_table = pn.widgets.Tabulator(
    value=construir_dataframe([]),
    pagination='remote',
    page_size=10,
    selectable=True,
    show_index=False,
    height=360,
    sizing_mode='stretch_width',
    width=620,
    visible=False,
    widths={
        'id_campanha': 80,
        'nome': 160,
        'regiao': 120,
        'data_inicio': 100,
        'data_fim': 100,
        'status': 100,
        'redes_sociais': 150,
        'id_instituicao': 100,
    },
)

id_campanha_input = pn.widgets.IntInput(name='ID Campanha', placeholder='Digite o ID', width=180)
nome_input = pn.widgets.TextInput(name='Nome', placeholder='Nome da campanha', width=260)
regiao_input = pn.widgets.TextInput(name='Região', placeholder='Região', width=200)
data_inicio = pn.widgets.DatePicker(name='Data Início', value=date.today(), width=200)
data_fim = pn.widgets.DatePicker(name='Data Fim', value=date.today(), width=200)
status_input = pn.widgets.TextInput(name='Status', placeholder='Ex: Ativa, Encerrada', width=220)
redes_sociais_input = pn.widgets.TextInput(name='Redes Sociais', placeholder='URLs ou descrição', width=280)

instituicao_opcoes = carregar_opcoes_instituicoes()
instituicao_dropdown = pn.widgets.Select(
    name='Instituição',
    options=instituicao_opcoes,
    value=next(iter(instituicao_opcoes.values())),
    width=280,
)

btn_add = pn.widgets.Button(name='Adicionar', button_type='default', width=120)
btn_edit = pn.widgets.Button(name='Editar', button_type='default', width=120)
btn_delete = pn.widgets.Button(name='Remover', button_type='default', width=120)
btn_list = pn.widgets.Button(name='Listar', button_type='default', width=120)

status_msg = pn.pane.Markdown('', styles={'font-weight': 'bold'})
titulo_lista = pn.pane.Markdown('## Lista de Campanhas', visible=False)


def atualizar_status(texto):
    status_msg.object = texto


def atualizar_tabela():
    campanhas_table.value = construir_dataframe(listar_campanhas())


def limpar_formulario():
    id_campanha_input.value = None
    nome_input.value = ''
    regiao_input.value = ''
    data_inicio.value = date.today()
    data_fim.value = date.today()
    status_input.value = ''
    redes_sociais_input.value = ''
    if instituicao_dropdown.options:
        instituicao_dropdown.value = next(iter(instituicao_dropdown.options.values()))


def get_form_data() -> dict:
    return {
        'id_campanha': id_campanha_input.value,
        'nome': nome_input.value.strip(),
        'regiao': regiao_input.value.strip(),
        'data_inicio': data_inicio.value,
        'data_fim': data_fim.value,
        'status': status_input.value.strip(),
        'redes_sociais': redes_sociais_input.value.strip() if redes_sociais_input.value else None,
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
        dados['id_instituicao'] is not None and dados['id_instituicao'] != 0,
    ])


def on_add(event):
    if not is_form_valid():
        atualizar_status('Preencha todos os campos obrigatórios corretamente.')
        return
    sucesso = adicionar_campanha(get_form_data())
    if sucesso:
        atualizar_status('Campanha adicionada com sucesso.')
        limpar_formulario()
        atualizar_tabela()
    else:
        atualizar_status('Erro ao adicionar a campanha. Verifique se o ID já está em uso.')


def on_edit(event):
    if id_campanha_input.value is None:
        atualizar_status('Informe o ID da campanha para editar.')
        return
    dados = get_form_data()
    sucesso = editar_campanha(dados['id_campanha'], {key: value for key, value in dados.items() if key != 'id_campanha'})
    if sucesso:
        atualizar_status('Campanha atualizada com sucesso.')
        limpar_formulario()
        atualizar_tabela()
    else:
        atualizar_status('Erro ao editar a campanha. Verifique se o ID existe.')


def on_delete(event):
    if id_campanha_input.value is None:
        atualizar_status('Informe o ID da campanha para remover.')
        return
    sucesso = excluir_campanha(id_campanha_input.value)
    if sucesso:
        atualizar_status('Campanha removida com sucesso.')
        limpar_formulario()
        atualizar_tabela()
    else:
        atualizar_status('Erro ao remover a campanha. Verifique se o ID existe.')


def on_list(event):
    if campanhas_table.visible:
        campanhas_table.visible = False
        titulo_lista.visible = False
        atualizar_status('Tabela oculta.')
        return
    atualizar_tabela()
    campanhas_table.visible = True
    titulo_lista.visible = True
    atualizar_status('Tabela exibida.')


def on_table_select(event):
    if not event.new:
        return
    selected = campanhas_table.selected_dataframe
    if selected.empty:
        return
    data = selected.iloc[0]
    id_campanha_input.value = int(data['id_campanha'])
    nome_input.value = str(data['nome'])
    regiao_input.value = str(data['regiao'])
    data_inicio.value = data['data_inicio']
    data_fim.value = data['data_fim']
    status_input.value = str(data['status'])
    redes_sociais_input.value = str(data['redes_sociais']) if pd.notna(data['redes_sociais']) else ''
    if data['id_instituicao'] in instituicao_dropdown.options.values():
        instituicao_dropdown.value = data['id_instituicao']


btn_add.on_click(on_add)
btn_edit.on_click(on_edit)
btn_delete.on_click(on_delete)
btn_list.on_click(on_list)

campanhas_table.param.watch(on_table_select, 'selection')

form_card = pn.Card(
    pn.pane.Markdown('## Formulário de Campanhas'),
    pn.Row(id_campanha_input, nome_input),
    pn.Row(regiao_input, instituicao_dropdown),
    pn.Row(data_inicio, data_fim),
    pn.Row(status_input, redes_sociais_input),
    pn.Row(btn_add, btn_edit, btn_delete, btn_list),
    status_msg,
    sizing_mode='stretch_width',
    width=520,
    margin=(0, 0, 0, 0),
)

conteudo = pn.Column(
    pn.pane.Markdown('# Gestão de Campanhas'),
    pn.Spacer(height=12),
    pn.Row(form_card, pn.Column(titulo_lista, campanhas_table), sizing_mode='stretch_width', align='start'),
)

conteudo.servable(title='Campanhas')
