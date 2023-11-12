import pymongo

# Elimina todos los duplicados y se queda con el ultimo documento

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
for doc in res:
    # print(f'{id} - {doc["count"]}')
    # encontrar documentos duplicados
    lst_duplicados = list(rent_col.find({
        "title": doc['_id']['title'],
        "origin": doc['_id']['origin'],
        "zone_name": doc['_id']['zone_name'],
        "total_area": doc['_id']['total_area'],
        "bathrooms": doc['_id']['bathrooms'],
        "bedrooms": doc['_id']['bedrooms']
        }))

    # mantiene el ultimo y eliminar duplicados
    for i, duplicado in enumerate(lst_duplicados):
        if i < len(lst_duplicados) - 1:
            rent_col.delete_one({"_id": duplicado["_id"]})


# cierra la conexion con mongodb
client.close()