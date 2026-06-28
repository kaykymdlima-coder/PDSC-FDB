import panel as pn

pn.extension()

pn.Column(
    "# Funcionou!",
    pn.widgets.Button(name="Teste")
).show()