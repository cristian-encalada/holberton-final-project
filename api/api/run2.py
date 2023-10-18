from api.factory import create_app

if __name__ == "__main__":
    app = create_app()

    # Configure the app with the MongoDB URI
    app.config['MONGO_URI'] = "mongodb+srv://alquivago:alquivago123@cluster0.hhicxbc.mongodb.net/alquivago?retryWrites=true&w=majority"

    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=5000)
