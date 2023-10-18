from alquivago.factory import create_app

import configparser


config = configparser.ConfigParser()
#config.read("sample_ini")#archivo con la ruta de la vase de datos tanto de testeo como oficial

if __name__ == "__main__":
    app = create_app()
    app.config['DEBUG'] = True
    # app.config['MONGO_URI'] = "mongodb+srv://alice:CheshireCat@prueba.emolc4y.mongodb.net/alquivago?retryWrites=true&w=majority"
    app.config['MONGO_URI'] = "mongodb+srv://alquivago:alquivago123@cluster0.hhicxbc.mongodb.net/alquivago?retryWrites=true&w=majority"

    app.run(host='0.0.0.0', port=5000)
