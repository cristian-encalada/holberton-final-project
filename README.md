run in local:
```
docker build -t hentype/standalone-chrome-airflow .
docker run -dit -p 4444:4444 -p 8080:8080 --shm-size="3g" --cpus=2.5 hentype/standalone-chrome-airflow
```

run from hub.docker:
```
docker pull hentype/standalone-chrome-airflow
```

start Airflow:
```
airflow standalone
```

* colocar token de github en archivo "/root/Alquivago/webscraping/upload.py":
```
token = os.environ['TOKEN'] = 'token de github'
```