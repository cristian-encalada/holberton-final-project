# Utiliza la imagen oficial de Ubuntu
FROM ubuntu:latest
# Actualiza los paquetes e instala Python 3 y pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip
# Instala git
RUN apt-get install -y git
# Instala requests
RUN pip install requests
# Instala flask-CORS, flassger y pymongo
RUN pip install -U flask-cors
RUN pip install flasgger
RUN pip install pymongo
# Agrega las dependencias adicionales
RUN pip install json
RUN pip install gitpython
# Expon el puerto 5000 para Flask (ajusta según sea necesario)
EXPOSE 5000
# Clonar repositorio
RUN git clone -b dev https://github.com/cristian-encalada/Alquivago.git
WORKDIR /Alquivago
RUN git pull
# Set the Flask app environment variable
ENV FLASK_APP=app.py
# Copia tu aplicación Flask a la imagen (asegúrate de tener app.py u otro nombre adecuado)
WORKDIR /Alquivago/api/
CMD ["flask", "run", "--host", "0.0.0.0"]
