from crud import listar_usuarios

usuarios = listar_usuarios()

for usuario in usuarios:
    print(usuario.nome_completo)