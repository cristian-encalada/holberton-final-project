from flask import Flask, Blueprint, request, jsonify
from api.db import get_rents, get_all
from api.utils import is_int, tex_none, chek_int, sorting, conversion
from datetime import datetime

app = Flask(__name__)
# Set the configuration variable
app.config['MONGO_URI'] = "mongodb+srv://alquivago:alquivago123@cluster0.hhicxbc.mongodb.net/alquivago?retryWrites=true&w=majority"

# Define the rents_api_v1 Blueprint
rents_api_v1 = Blueprint('rent_api_v1', 'rent_api_v1', url_prefix='/api/v1/rent')


conv = conversion()

@rents_api_v1.route('/', methods=['GET'])
def api_get_all():
    RENTS_PER_PAGE = 10

    page = is_int(request.args.get('page'))
    if page is None or page == 0:
        page = 1
    sort = sorting(request.args.get('orden'))

    print(page)

    (rents, total_num_entries) = get_all(
        conv, sort, page, rents_per_page=RENTS_PER_PAGE)

    response = {
    "rents": rents,
    "page": page,
    "filters": sort,
    "entries_per_page": RENTS_PER_PAGE,
    "total_results": total_num_entries,
    }

    return jsonify(response)

@rents_api_v1.route('/filtro', methods=['GET'])
def api_get_rent():
    RENTS_PER_PAGE = 10

    page = is_int(request.args.get('page'))
    if page is None or page == 0:
        page = 1
    filters = {
        "types": chek_int(request.args.get('tipos')),
        "zones": tex_none(request.args.get('zonas')),
        "bedrooms": chek_int(request.args.get('dormitorios')),
        "bathrooms": chek_int(request.args.get('baños')),
        "sort": sorting(request.args.get('orden'))} #orden=zonas:1,types:-1

    currency = request.args.get('moneda')
    price_min_max = chek_int(request.args.get('min_max'))
    area_min_max = chek_int(request.args.get('area'))

    if currency is not None and price_min_max is not None and len(price_min_max) == 2:
        filters["price"] = {
            "currency" : request.args.get('moneda'),
            "min": price_min_max[0],
            "max": price_min_max[1],
            "conv": conv}
    elif currency is not None and price_min_max is None:
        filters["currency"] = currency
    if area_min_max is not None and len(area_min_max) == 2:
        filters["area"] = {
            "min": area_min_max[0],
            "max": area_min_max[1]}

    print(filters)

    (rents, total_num_entries, query) = get_rents(
        conv, filters, page, rents_per_page=RENTS_PER_PAGE)

    response = {
        "rents": rents,
        "page": page,
        "filters": query,
        "entries_per_page": RENTS_PER_PAGE,
        "total_results": total_num_entries,
    }

    return jsonify(response)

# Register the Blueprint with the app
app.register_blueprint(rents_api_v1)

# if __name__ == '__main__':
#    app.run(debug=True)