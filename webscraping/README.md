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

* configurar variable de entorno del TOKEN de github:
```
root@b7831ca266f9:/root/Alquivago/webscraping# export TOKEN=tokendegithub
```