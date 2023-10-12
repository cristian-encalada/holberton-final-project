# webscraping


selenium/standalone-chrome + Apache-Airflow

local:
```
docker build -t hentype/custom .
docker run -dit -p 4444:4444 -p 7900:7900 -p 8080:8080 --shm-size="2g" hentype/custom
```

https://hub.docker.com/u/hentype:
```
docker pull hentype/custom:latest
```

start Airflow:
```
airflow standalone
```