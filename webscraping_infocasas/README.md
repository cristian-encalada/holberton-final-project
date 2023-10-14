Dockerfile: selenium/standalone-chrome + Apache-Airflow

run in local:
```
docker build -t hentype/custom .
docker run -dit -p 4444:4444 -p 7900:7900 -p 8080:8080 --shm-size="2g" hentype/custom
```

run from hub.docker:
```
docker pull hentype/custom:latest
```

start Airflow:
```
airflow webserver
airflow standalone
```