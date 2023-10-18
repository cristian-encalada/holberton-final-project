def sort_apply(rent, sort, conv):
    """apply sort"""
     #ordenamiento 
    sorts = {}
    if sort is not None:
        type = {"area": "total_area", "price": "price_conv"}
        for o, t in sort.items():
            if o in type:
                sorts[type[o]] = t
    if "price" in sort and rent:
        for document in rent:
            document["price_conv"] = document["price"]
            if document["currency"] == "USD":
                document["price_conv"] = document["price"] * conv
    
    if len(sorts) != 0:
        def custom_key(document):
            return tuple(t * document[o] for o, t in sorts.items())
        rent = sorted(rent, key=custom_key)
    return(rent)

def delete__id(rent):
    """delete _id and price_conv"""
    if rent:
        for document in rent:
            del document["_id"] #delete the _id (ObjectID)
            if "price_conv" in document:
                del document["price_conv"]
    return rent
