# Utiliza la imagen oficial de Ubuntu
FROM ubuntu:latest
# Actualiza los paquetes e instala Python 3 y pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip
# Instala Flask, Flask-PyMongo y Flask-CORS usando pip
RUN pip3 install flask flask-pymongo flask-cors
# Instala git
RUN apt-get install -y git
# Expon el puerto 5000 para Flask (ajusta según sea necesario)
EXPOSE 5000
# Clonar repositorio
RUN git clone -b dev https://github.com/cristian-encalada/Alquivago.git
WORKDIR /Alquivago
RUN git pull
# Copia tu aplicación Flask a la imagen (asegúrate de tener app.py u otro nombre adecuado)
WORKDIR /Alquivago/api
CMD ["python3", "run.py", "run", "--host", "0.0.0.0"]
