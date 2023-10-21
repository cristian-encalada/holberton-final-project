import re

def f_currency(currency):
    """
    currency es un string,
    retorno un diccionario con la consulta
    """
    types = ["UYU", "USD"]
    if currency in types:
        return({"currency": currency})
    return (None)


def f_types(types):
    """
    typres es una lista de int, normalisadas
    [num , ...],
    retorno un diccionario con la consulta
    """
    from modules.db import db
    
    """property_types = list(db.property_types_col.find({"property_types": {"$exists": True}}))
    property_types = property_types[0]['property_types']
    print(types)
    print(property_types)
    result = [doc['name'] for doc in property_types if doc['id'] in types]"""
    
    result = [doc["name"] for doc in db.property_types_col.find({"id": {"$in": types}}, {"name": 1, "_id": 0})]


    return({"property_type": {"$in": result}})


def f_zones(zones):
    """
    zones es una lista de strigs, sin normalisar por completo
    ["no_normalisado"(none), "normalisado", ...],
    retorno un diccionario con la consulta
    """
    
    from modules.db import db
    result = [doc["zona"] for doc in db.zonas_mvd_col.find({"id": {"$in": zones}}, {"zona": 1, "_id": 0})]


    escaped_zones = [re.escape(zone) for zone in result]
    regex_pattern = "|".join(escaped_zones)
    return({"zone_name": {"$regex": regex_pattern, "$options": "i"}})# "i" para que sea insensible a mayúsculas/minúsculas


def f_bedrooms(bedrooms):
    """
    bedrooms es una lista con numeros [num, ...] si contiene el valor
    more_bedrooms entonces busca los resultados valores superiores al mismo,
    retorno un diccionario con la consulta
    """
    more_bedrooms = 4

    list_b = [element for element in bedrooms if element is not None and element <= more_bedrooms]
    if len(list_b) > 0:
        bedrooms = {"$or": [{"bedrooms": {"$in": list_b}}]}
        if more_bedrooms in list_b:
            bedrooms["$or"].append({"bedrooms": {"$gt": more_bedrooms}})
        return(bedrooms)


def f_bathrooms(bathrooms):
    """
    bathrooms es una lista con numeros [num, ...] si contiene el valor
    more_bathrooms entonces busca los resultados valores superiores al mismo,
    retorno un diccionario con la consulta
    """
    more_bathrooms = 3
    
    list_b = [element for element in bathrooms if element != None and element <= more_bathrooms]
    if len(list_b) > 0:
        bathrooms = {"$or": [{"bathrooms": {"$in": list_b}}]}
        if more_bathrooms in list_b:
            bathrooms["$or"].append({"bathrooms": {"$gt": more_bathrooms}})
        return(bathrooms)

def f_price(price_data):
    """
    price_data es un diccionario con tres valores 
    {"currency": "tipo", "min": int(none), "max": int(none), "conv": int},
    retorno un diccionario con la consulta
    """    
    price = { "$or": [
            {"currency": "UYU", "price": {}},
            {"currency": "USD", "price": {}}
        ]}
    
    price_min = price_data["min"]
    price_max = price_data["max"]
    conv = price_data["conv"]

    if price_data["currency"] == "UYU":
        if price_min is not None:
            conversion_min = price_min / conv
            price["$or"][0]["price"]["$gte"] = price_min
            price["$or"][1]["price"]["$gte"] = conversion_min
        if price_max is not None:
            conversion_max = price_max / conv
            price["$or"][0]["price"]["$lte"] = price_max
            price["$or"][1]["price"]["$lte"] = conversion_max
    elif price_data["currency"] == "USD":
        if price_min is not None:
            conversion_min = price_min * conv
            price["$or"][0]["price"]["$gte"] = conversion_min
            price["$or"][1]["price"]["$gte"] = price_min
        if price_max is not None:
            conversion_max = price_max * conv
            price["$or"][0]["price"]["$lte"] = conversion_max
            price["$or"][1]["price"]["$lte"] = price_max
    else:
        return(None)
    if price_min is not None or price_max is not None:
        return(price)
    else:
        return(f_currency(price_data["currency"]))


def f_area(area_data):
    """
    area_data es un diccionario con 2 valores
    {"min": int(none), "max": int(none)},
    retorno un diccionario con la consulta
    """
    area = {"total_area": {}}
    area_min = area_data["min"]
    area_max = area_data["max"]
    if area_min is not None:
        area["total_area"]["$gte"] = area_min
    if area_max is not None:
        area["total_area"]["$lte"] = area_max
    if area_min is not None or area_max is not None:
        return(area)
