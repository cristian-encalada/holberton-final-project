from github import Github
import os

# token = os.environ['TOKEN'] = 'tokengithub'

# variable de entorno TOKEN
if "TOKEN" in os.environ:
    token = os.environ["TOKEN"]
else:
    print("Environment variable TOKEN is not defined. ( export TOKEN=yourtoken )")

g = Github(token)

# obtener el repositorio
repo = g.get_repo("cristian-encalada/Alquivago")
# rama
branch_name = "main"

# clave: ruta local , valor: ruta repositorio
json_files = {
    "/gallito.json": "data/gallito.json",
    "/infocasas.json": "data/infocasas.json",
    "/extracted_data.json": "data/mercadolibre.json"
}

# leer archivo json
for k, v in json_files.items():

    with open(k, 'r') as op:
        contenido = op.read()

    # obtener el contenido del archivo en GitHub
    file_content = repo.get_contents(v, ref=branch_name)

    if file_content:
        # si el archivo existe
        repo.update_file(
            path=v,
            message="updated JSON",
            content=contenido,
            branch=branch_name,
            sha=file_content.sha
        )
    else:
        # si el archivo no existe
        repo.create_file(
            path=v,
            message="updated JSON",
            content=contenido,
            branch=branch_name
        )
