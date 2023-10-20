from github import Github
import os

# token github desde variable de entorno
token = os.environ['TOKEN'] = 'gha_jyFmn2tDUKcRwtrKduF2LaOmWzkNnk0MbDyA'

# chequear si no se agrega el token
if token is None:
    raise ValueError("GitHub token needed.")

g = Github(token)

# obtener el repositorio
repo = g.get_repo("cristian-encalada/Alquivago")
# rama
branch_name = "main"

# clave: ruta local , valor: ruta repositorio
json_files = {
    "/root/airflow/dags/gallito.json": "data/gallito.json",
    "/root/airflow/dags/infocasas.json": "data/infocasas.json",
    "/extracted_data.json": "data/mercadolibre.json"
}

# leer archivo json
for k, v in json_files.items():
    with open(k, 'r') as op:
        contenido = op.read()

    try:
        # obtener el contenido del archivo en GitHub
        file_content = repo.get_contents(v, ref=branch_name)

        # si el archivo existe
        repo.update_file(
            path=v,
            message="updated JSON",
            content=contenido,
            branch=branch_name,
            sha=file_content.sha
        )
    except Exception as e:
        # si el archivo no existe
        repo.create_file(
            path=v,
            message="updated JSON",
            content=contenido,
            branch=branch_name
        )
