import json
import requests
import git
import os


def conversion():
    """
    Retrieves the currency conversion rate between two currencies.
    In this case, the function fetches the conversion rate between USD and UYU.
    If the API call fails, it returns a default value of 40 as a sample conversion rate.
    """
    # Obtener la ruta del directorio actual del script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta del archivo cambio.json
    data_directory = os.path.abspath(os.path.join(current_directory, "../data"))
    cambio_json_path = os.path.join(data_directory, "cambio.json")

    # Verificar y crear los directorios necesarios si no existen
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    access_key = '108becf3bf3c99a76d9548282aa88dba51012e8b'
    base_currency = 'USD'
    target_currency = 'UYU'

    url = f'https://api.getgeoapi.com/v2/currency/convert?api_key={access_key}&from={base_currency}&to={target_currency}&amount=1&format=json'
    response = requests.get(url)

    if response.status_code == 200:
        conversion_data = response.json()
        if conversion_data['status'] == 'success':
            converted_value = float(conversion_data['rates']['UYU']['rate'])
            with open(cambio_json_path, 'w') as file:
                json.dump({"rate": converted_value}, file)
            # Agregar cambios al repositorio de Git
            data_directory = os.path.abspath(os.path.join(data_directory, "../"))
            cambio_json_path = os.path.join(data_directory, "data/cambio.json")
            repo = git.Repo(data_directory)
            repo.git.add(cambio_json_path)
            repo.index.commit("Update the file: cambio.json")
            origin = repo.remote(name='origin')
            origin.push()
            return converted_value

    # Si hay un error en la llamada a la API, se guarda el valor predeterminado
    default_value = 40
    with open(cambio_json_path, 'w') as file:
        json.dump({"rate": default_value}, file)
    # Agregar cambios al repositorio de Git
    data_directory = os.path.abspath(os.path.join(data_directory, "../"))
    cambio_json_path = os.path.join(data_directory, "data/cambio.json")
    repo = git.Repo(data_directory)
    repo.git.add(cambio_json_path)
    repo.index.commit("No more API queries for conversion. Sample value: 40")
    origin = repo.remote(name='origin')
    origin.push()
    return default_value

# Ejecuta la función
conversion()
