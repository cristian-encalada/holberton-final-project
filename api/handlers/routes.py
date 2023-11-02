# from modules import modules
from flask import abort, jsonify, make_response, request
from modules.utils import is_int, chek_int, tex_none, sorting, cambio_call
from modules.db import get_rents, get_all, get_map_operation, get_cont_zone_v2
from flasgger import Swagger
from flasgger.utils import swag_from

# Common prefix for all API routes
api_prefix = '/api/v1/'

def configure_routes(app):
    @app.route(api_prefix + '<type_operations>/', methods=['GET'], strict_slashes=False)
    @swag_from('documentation/rent/api_get_all.yml', methods=['GET'])
    def api_get_all(type_operations):
        RENTS_PER_PAGE = 10
        conv = cambio_call()

        page = is_int(request.args.get('page'))
        if page is None or page == 0:
            page = 1
        sort = sorting(request.args.get('orden'))

        print(page)

        (rents, total_num_entries) = get_all(
            type_operations, conv, sort, page, rents_per_page=RENTS_PER_PAGE)

        response = {
        "rents": rents,
        "page": page,
        "entries_per_page": RENTS_PER_PAGE,
        "total_results": total_num_entries,
        }

        return jsonify(response)

    @app.route(api_prefix + '<type_operations>/inmuebles', methods=['GET'], strict_slashes=False)
    @swag_from('documentation/rent/api_get_rent.yml', methods=['GET'])
    def api_get_rent(type_operations):
        RENTS_PER_PAGE = 10
        conv = cambio_call()

        page = is_int(request.args.get('page'))
        if page is None or page == 0:
            page = 1
        filters = {
            "types": chek_int(request.args.get('tipos')),
            "zones": chek_int(request.args.get('zonas')),
            "bedrooms": chek_int(request.args.get('dormitorios')),
            "bathrooms": chek_int(request.args.get('baños')),
            "sort": sorting(request.args.get('orden'))} #orden=zonas:1,types:-1

        currency = request.args.get('moneda')
        price_min_max = chek_int(request.args.get('min_max'))
        area_min_max = chek_int(request.args.get('area'))

        if price_min_max is not None and len(price_min_max) == 2:
            filters["price"] = {
                "currency" : currency,
                "min": price_min_max[0],
                "max": price_min_max[1],
                "conv": conv}
        else:
            filters["currency"] = currency

        if area_min_max is not None and len(area_min_max) == 2:
            filters["area"] = {
                "min": area_min_max[0],
                "max": area_min_max[1]}

        (rents, total_num_entries) = get_rents(
            type_operations, conv, filters, page, rents_per_page=RENTS_PER_PAGE)

        response = {
            "rents": rents,
            "page": page,
            "entries_per_page": RENTS_PER_PAGE,
            "total_results": total_num_entries,
        }

        return jsonify(response)
    
    @app.route(api_prefix + '<type_operations>/mapa/', defaults={'list_zone': None}, methods=['GET'], strict_slashes=False)
    @app.route(api_prefix + '<type_operations>/mapa/<list_zone>', methods=['GET'], strict_slashes=False)
    @swag_from('documentation/rent/api_get_all_map.yml', methods=['GET'])
    def api_get_map(type_operations, list_zone):

        if list_zone is None:
            zones = []
        else:
            zones = chek_int(list_zone)

        (rents, total_num_entries) = get_map_operation(
            type_operations, zones)
        
        response = {
            "rents": rents,
            "total_results": total_num_entries,
        }
        
        return jsonify(response)
    
    @app.route(api_prefix + '<type_operations>/conteo_zona', methods=['GET'], strict_slashes=False)
    @swag_from('documentation/rent/api_get_cont_zones.yml', methods=['GET'])
    def get_cont_zones(type_operations):

        (rents, total_num_entries) = get_cont_zone_v2(
            type_operations)
        
        response = {
            "rents": rents,
            "total_results": total_num_entries,
        }
        
        return jsonify(response)
    
