import re

def f_operation(type_operations):
    """
    Construct a MongoDB query based on the type of property operation.

    This function takes a string, type_operations, as input, which represents the type of
    property operation, such as "rent" or "buy". If the type of operation is "rent", the function
    returns the corresponding collection name, "rent_col". If the type of operation is "buy", the
    function returns the collection name "buy_col". If the type of operation is not recognized,
    the function prepares and returns default values for rents, total number of rents, and an
    empty query dictionary.

    Args:
    type_operations (str): A string representing the type of property operation.

    Returns:
    str or tuple: If the type of operation is recognized, the function returns the corresponding
    collection name. If the type of operation is not recognized, the function returns a tuple
    containing default values for rents, total number of rents, and an empty query dictionary.
    """
    if "rent" == type_operations:
        return "rent_col"
    elif "buy" == type_operations:
        return "buy_col"
    else:
        rents = []
        total_num_rents = 0
        query = {}
        return (rents, total_num_rents)

def f_currency(currency):
    """
    Construct a MongoDB query for filtering based on currency type.

    This function takes a string, currency, as input, which represents the currency type.
    It checks whether the provided currency type is one of the recognized types, i.e., "UYU"
    or "USD". If the currency type is valid, the function returns a dictionary containing the
    MongoDB query for filtering based on the currency type. If the currency type is not recognized,
    it returns None.

    Args:
    currency (str): A string representing the currency type.

    Returns:
    dict or None: A dictionary containing the constructed MongoDB query for filtering based on
    the currency type, or None if the currency type is not recognized.
    """
    types = ["UYU", "USD"]
    if currency in types:
        return({"currency": currency})
    return (None)


def f_types(types):
    """
    Construct a MongoDB query for filtering based on property type IDs.

    This function takes a list, types, as input, which contains integers representing
    normalized property type IDs. The function queries the database to retrieve the
    corresponding property type names based on the provided IDs.

    The function returns a dictionary containing the constructed MongoDB query for
    filtering based on the property type names, considering the normalized property type
    IDs provided in the list.

    Args:
    types (list): A list of integers representing normalized property type IDs.

    Returns:
    dict: A dictionary containing the constructed MongoDB query for filtering based on
    the property type names.
    """
    from modules.db import db
    
    result = [doc["name"] for doc in db.property_types_col.find({"id": {"$in": types}}, {"name": 1, "_id": 0})]


    return({"property_type": {"$in": result}})


def f_zones(zones):
    """
    Construct a MongoDB query for filtering based on zone IDs.

    This function takes a list, zones, as input, which contains integers representing
    normalized zone IDs in the collection 'zonas_mvd_col'. The function queries the
    database to retrieve the corresponding zone names based on the provided IDs. It
    escapes special characters in the zone names and creates a regex pattern to match
    the names in a case-insensitive manner.

    The function returns a dictionary containing the constructed MongoDB query for
    filtering based on the zone names, considering the normalized zone IDs provided in
    the list.

    Args:
    zones (list): A list of integers representing normalized zone IDs in the 'zonas_mvd_col' collection.

    Returns:
    dict: A dictionary containing the constructed MongoDB query for filtering based
    on the zone names.
    """
    
    from modules.db import db
    result = [doc["zona"] for doc in db.zonas_mvd_col.find({"id": {"$in": zones}}, {"zona": 1, "_id": 0})]


    escaped_zones = [re.escape(zone) for zone in result]
    regex_pattern = "|".join(escaped_zones)
    return({"zone_name": {"$regex": regex_pattern, "$options": "i"}})# "i" para que sea insensible a mayúsculas/minúsculas


def f_cities(cities):
    """
    Construct a MongoDB query for filtering based on city names.

    This function takes a list, cities, as input, which contains strings representing
    city names. The list may contain both normalized and non-normalized city names.
    The function constructs a MongoDB query for filtering documents based on the city
    names. It escapes special characters in the city names and creates a regex pattern
    to match the names in a case-insensitive manner.

    The function returns a dictionary containing the constructed MongoDB query for
    filtering based on the city names, considering both normalized and non-normalized
    names in the list.

    Args:
    cities (list): A list of strings representing city names, both normalized and
    non-normalized.

    Returns:
    dict: A dictionary containing the constructed MongoDB query for filtering based
    on the city names.
    """

    escaped_cities = [re.escape(city) for city in cities]
    regex_pattern = "|".join(escaped_cities)
    return({"zone_name": {"$regex": regex_pattern, "$options": "i"}})# "i" para que sea insensible a mayúsculas/minúsculas


def f_bedrooms(bedrooms):
    """
    Construct a MongoDB query for filtering based on the number of bedrooms.

    This function takes a list, bedrooms, as input, which contains numerical values
    representing the number of bedrooms in a property, e.g., [num, ...]. If the list
    contains the value 'more_bedrooms', the function searches for results with values
    greater than the specified threshold.

    The function constructs a MongoDB query for filtering documents based on the number
    of bedrooms. It handles scenarios where the number of bedrooms is within a specified
    range or exceeds a particular threshold ('more_bedrooms').

    The function returns a dictionary containing the constructed MongoDB query for
    filtering based on the number of bedrooms, considering the presence of the
    'more_bedrooms' value and the list of bedroom numbers provided.

    Args:
    bedrooms (list): A list containing numerical values representing the number of
    bedrooms in a property.

    Returns:
    dict: A dictionary containing the constructed MongoDB query for filtering based
    on the number of bedrooms.
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
    Construct a MongoDB query for filtering based on the number of bathrooms.

    This function takes a list, bathrooms, as input, which contains numerical values
    representing the number of bathrooms in a property, e.g., [num, ...]. If the list
    contains the value 'more_bathrooms', the function searches for results with values
    greater than the specified threshold.

    The function constructs a MongoDB query for filtering documents based on the number
    of bathrooms. It handles scenarios where the number of bathrooms is within a
    specified range or exceeds a particular threshold ('more_bathrooms').

    The function returns a dictionary containing the constructed MongoDB query for
    filtering based on the number of bathrooms, considering the presence of the
    'more_bathrooms' value and the list of bathroom numbers provided.

    Args:
    bathrooms (list): A list containing numerical values representing the number of
    bathrooms in a property.

    Returns:
    dict: A dictionary containing the constructed MongoDB query for filtering based
    on the number of bathrooms.
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
    Construct a MongoDB query for filtering based on the price.

    This function takes a dictionary, price_data, as input with the following keys:
    "currency" (string), "min" (int or None), "max" (int or None), and "conv" (int).
    The "currency" key represents the type of currency, "min" and "max" keys represent
    the optional minimum and maximum values for the price, and "conv" represents the
    conversion rate between two currencies.

    The function constructs a MongoDB query for filtering documents based on the price
    field. It handles conversions between different currencies based on the provided
    conversion rate. If a minimum or maximum value is provided, it adds appropriate
    filters for the price based on the currency type and the conversion rate.

    The function returns a dictionary containing the constructed MongoDB query for
    filtering based on the price, considering the currency and conversion rate provided.

    Args:
    price_data (dict): A dictionary with keys "currency", "min", "max", and "conv"
    representing the currency type, minimum and maximum values for the price, and the
    conversion rate.

    Returns:
    dict: A dictionary containing the constructed MongoDB query for filtering based
    on the price and considering the currency and conversion rate.
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
    Construct a MongoDB query for filtering based on the total area.

    This function takes a dictionary, area_data, as input with optional minimum
    and maximum values for the total area:
    {"min": int or None, "max": int or None}.

    It constructs a MongoDB query for filtering documents based on the total
    area field. If a minimum value is provided, it adds a filter for total area
    greater than or equal to the specified minimum. If a maximum value is
    provided, it adds a filter for total area less than or equal to the
    specified maximum.

    The function returns a dictionary containing the constructed query for the
    total area filter, which can be used for querying a MongoDB collection.

    Args:
    area_data (dict): A dictionary with optional "min" and "max" keys,
    representing the minimum and maximum values for the total area.

    Returns:
    dict: A dictionary containing the constructed MongoDB query for filtering
    based on the total area.
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
