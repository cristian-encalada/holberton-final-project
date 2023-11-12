import pymongo

# Muestra en consola todos los duplicados

atlas_uri = "mongodb+srv://alquivago:alquivago123@cluster0.hhicxbc.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(atlas_uri)

# base de datos y coleccion
db = client["alquivago_dev"]
rent_col = db["rent_col"]


# consulta de agregacion para encontrar los duplicados
res = rent_col.aggregate([
    {"$group": {
        "_id": {
            "title": "$title",
            "origin": "$origin",
            "zone_name": "$zone_name",
            "total_area": "$total_area",
            "bathrooms": "$bathrooms",
            "bedrooms": "$bedrooms"
        },
        "count": {"$sum": 1}
    }},
    {"$match": {
        "count": {"$gt": 1}
    }}
])


# iterar sobre el resultado
lst_duplicados = []
for doc in res:
    title = doc['_id']['title'],
    origin = doc['_id']['origin'],
    zone_name = doc['_id']['zone_name']
    total_area = doc['_id']['total_area']
    bathrooms = doc['_id']['bathrooms']
    bedrooms = doc['_id']['bedrooms']

    # list documentos duplicados
    lst_duplicados.append(rent_col.find(doc['_id']))


if len(lst_duplicados) == 0:
     print("No hay duplicados")
else:
    # muestra documentos duplicados
    for duplicado in lst_duplicados:
        for documento in duplicado:
            print(documento)


# cierra la conexion con mongodb
client.close()