# Alquivago - 1st MVP done

Pasos para correr localmente el proyecto

## Ejecutar en el contenedor de docker

### 1. Almacenar los datos scrapeados en Mongodb

Directorio: 
```sh
Alquivago/mongodb
```
Commando: 

```python
python3 store_data.py
```

### 2. Ejecutar flask para la API interna


Directorio: 
```sh
Alquivago/api/simple_get
```
Commando: 

```python
python3 app.py
```

```
http://127.0.0.1:5000/api/data
```

## Ejecutar sobre windows

### 3. Levantar el Frontend (React y Vite)

#### 3.0 Clonar el repositorio (dev branch)

```sh
 git clone -b dev https://github.com/cristian-encalada/Alquivago.git
```

#### 3.1 Instalar nvm (nvm-setup.exe)

https://github.com/coreybutler/nvm-windows/releases


```sh
nvm install latest
nvm use 20.7.0
```
output
```sh
Now using node v20.7.0 (64-bit)
```
Desde el directorio

```sh
Alquivago\vite-project
```

Ejecutar el comando

```sh
npm install
```

Levantar el Frontend (Vite/React)

```
npm run dev
```

Acceder a la URL

```
http://localhost:5173/
```

# Run docker compose with all containers (flask, react, mongodb, selenium)

To build and run all services defined in your docker-compose.yml file:
```sh
docker-compose up -d
```

To stop and remove all containers defined in your docker-compose.yml file:
```
docker-compose down
```
