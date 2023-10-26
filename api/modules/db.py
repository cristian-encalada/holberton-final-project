from modules.f_filters import f_operation, f_area, f_bathrooms, f_bedrooms, f_currency, f_price, f_types, f_zones
from modules.sort_delete import sort_apply, delete__id
import re

from flask import current_app, g
from werkzeug.local import LocalProxy
from pymongo import MongoClient


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        mongo_uri = current_app.config['MONGO_URI']  # Get MongoDB URI from Flask config
        client = MongoClient(mongo_uri)
        db = g._database = client.get_database()
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def build_query_sort_project(filters):
    """
    Builds the `query` predicate, `sort` and `projection` attributes for a given
    filters dictionary.
    """
    sort = filters["sort"]
    query = {}
    project = None # elije que datos traer, de momento traeremos todos

    #filtrado
    filters_list = []
    f_filters = {
        "currency": f_currency,
        "types": f_types,
        "zones": f_zones,
        "bedrooms": f_bedrooms,
        "bathrooms": f_bathrooms,
        "price": f_price,
        "area": f_area}
    for k, v in filters.items():
        if v is not None and k in f_filters.keys():
            add = f_filters[k](v)
            if add is not None:
                filters_list.append(add)
    
    if "price" not in sort and "price" in filters:
        sort["price"] = 1# orden base acendente
    
    if "area" not in sort and "area" in filters:
        sort["area"] = -1# orden base desendente
    
    #filtro de proximidad con la latitud y longitud
    
    if filters_list:
        query["$and"] = filters_list
    
    return query, sort, project




def get_rents(type_operations, conv, filters, page, rents_per_page):
    """
    Returns a cursor to a list of rental property documents.

    Based on the page number and the number of properties per page, the result may
    be skipped and limited.

    The `filters` from the API are passed to the `build_query_sort_project`
    method, which constructs a query, sort, and projection, and then that query
    is executed by this method (`get_rental_properties`).

    Returns 2 elements in a tuple: (properties, total_num_properties)
    """
    propertys = f_operation(type_operations)
    if type(propertys) is not str:
        return propertys

    query, sort, project = build_query_sort_project(filters)

    if project:
        cursor = db[propertys].find(query, project)
    else:
        cursor = db[propertys].find(query)
    
    rents = sort_apply(list(cursor), sort, conv)

    total_num_rents = len(rents)
    skip = (page - 1) * rents_per_page


    if (skip + rents_per_page) <= total_num_rents:
        rents = rents[skip:skip + rents_per_page]
    elif skip <= total_num_rents:
        rents = rents[skip:]
    else:
        rents = []
    rents = delete__id(rents)

    return (rents, total_num_rents, query)


def get_all(type_operations, conv, sort, page, rents_per_page):
    """
    List all type of rents
    """

    propertys = f_operation(type_operations)
    if type(propertys) is not str:
        return propertys
    
    cursor = db[propertys].find()

    rents = sort_apply(list(cursor), sort, conv)

    total_num_rents = len(rents)
    skip = (page - 1) * rents_per_page


    if (skip + rents_per_page) <= total_num_rents:
        rents = rents[skip:skip + rents_per_page]
    elif skip <= total_num_rents:
        rents = rents[skip:]
    else:
        rents = []
    rents = delete__id(rents)
    query = {}#eliminar

    return (rents, total_num_rents, query)


def get_map_operation(type_operations, zones):
    """List all propertys to show in the map"""
    propertys = f_operation(type_operations)
    if type(propertys) is not str:
        return propertys
    
    project = {
        "id": 1,
        "url_link": 1,
        "zone_name": 1,
        "location.latitude": 1,
        "location.longitude": 1,
        "origin": 1,
        "operation_type": 1,
        "price": 1,
        "currency": 1,
        "_id": 0}
    query = f_zones(zones)
    rents = list(db[propertys].find(query,project))

    total_num_rents = len(rents)
    

    return (rents, total_num_rents, query)


def get_cont_zone(type_operations):
    """cont all the properties in all zones"""

    propertys = f_operation(type_operations)
    if type(propertys) is not str:
        return propertys
    
    project = {
        "zona": 1,
        "_id": 0}
    query = {}
    all_zones = list(db.zonas_mvd_col.find(query,project))

    cont = 0
    for zone in all_zones:
        escaped_zones = re.escape(zone["zona"])
        zone["cantidad"] = db[propertys].count_documents({"zone_name": {"$regex": escaped_zones, "$options": "i"}})
        cont += zone["cantidad"]

    total_num_rents = 0 #eliminar

    return (all_zones, total_num_rents, cont)


def get_conteo_municipio(type_operations):
    """cont all the properties in all zones"""

    propertys = f_operation(type_operations)
    if type(propertys) is not str:
        return propertys
    
    project = {
        "zona": 1,
        "_id": 0}
    municipios = ["A", "B", "C", "CH", "D", "E", "F", "G"]
    escaped_municipios = [re.escape(municipio) for municipio in municipios]
    
    all_municipios = {}
    for municipio in escaped_municipios:
        query = {"municipio": {"$regex": municipio, "$options": "i"}}# "i" para que sea insensible a mayúsculas/minúsculas
        all_municipios[municipio] = list(db.zonas_mvd_col.find(query,project))

    cont = 0
    result = []
    for municipio, list_zone in all_municipios.items():
        res = {}
        escaped_zones = [re.escape(zone["zona"]) for zone in list_zone]
        regex_pattern = "|".join(escaped_zones)
        res["cantidad"] = db[propertys].count_documents({"zone_name": {"$regex": regex_pattern, "$options": "i"}})
        res["municipio"] = municipio
        cont += res["cantidad"]
        result.append(res)

    total_num_rents = 0 #eliminar

    return (result, total_num_rents, cont)