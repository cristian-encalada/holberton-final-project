import requests
from bs4 import BeautifulSoup
import json

# Send an HTTP GET request to the URL
url = "https://es.wikipedia.org/wiki/Anexo:Barrios_de_Montevideo"
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, "html.parser")

# Find the last table containing the data
tables = soup.find_all("table", {"class": "wikitable"})  # Find all tables with class "wikitable"
last_table = tables[-1]  # Get the last table

# Initialize a list to store the extracted data
zonas = []

# Extract data from the last table
for row in last_table.find_all("tr")[1:]:  # Skip the header row
    columns = row.find_all("td")
    if len(columns) >= 4:
        zona_id = int(columns[0].text.strip())
        zona_name = columns[1].find("a").text.strip()
        ccz = columns[2].text.strip()
        municipio = columns[3].text.strip()

        zona_data = {
            "id": zona_id,
            "zona": zona_name,
            "centro comunal zonal": ccz,
            "municipio": municipio
        }

        zonas.append(zona_data)

# Create a dictionary to store the data
data = {"zonas": zonas}

# Save the data in a JSON file
with open("zonas_montevideo.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Data saved to zonas_montevideo.json")
