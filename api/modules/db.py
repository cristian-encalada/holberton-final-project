from modules.f_filters import f_operation, f_area, f_bathrooms, f_bedrooms, f_currency, f_price, f_types, f_zones
from modules.sort import sort_apply
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
    project = {"_id": 0} # elije que datos traer, de momento traeremos todos

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

    return (rents, total_num_rents)


def get_all(type_operations, conv, sort, page, rents_per_page):
    """
    List all type of rents
    """

    propertys = f_operation(type_operations)
    if type(propertys) is not str:
        return propertys
    
    cursor = db[propertys].find({},{"_id": 0})

    rents = sort_apply(list(cursor), sort, conv)

    total_num_rents = len(rents)
    skip = (page - 1) * rents_per_page


    if (skip + rents_per_page) <= total_num_rents:
        rents = rents[skip:skip + rents_per_page]
    elif skip <= total_num_rents:
        rents = rents[skip:]
    else:
        rents = []
    query = {}#eliminar

    return (rents, total_num_rents)


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
    

    return (rents, total_num_rents)


def get_cont_zone_v2(type_operations):
  """Count all the properties in all zones"""

  propertys = f_operation(type_operations)
  if type(propertys) is not str:
    return propertys

  pipeline = [
      {
          "$match": {}  # You can add any filtering conditions here
      },
      {
          "$group": {
              "_id": "$zone_name",
              "cantidad": {"$sum": 1}
          }
      },
      {
          "$project": {
              "zona": "$_id",
              "_id": 0,
              "cantidad": 1
          }
      }
  ]

  result = list(db[propertys].aggregate(pipeline))

  total_num_rents = sum(item["cantidad"] for item in result)

  return (result, total_num_rents)
