Dockerfile: selenium/standalone-chrome + Apache-Airflow

run in local:
```
docker build -t hentype/custom .
docker run -dit -p 4444:4444 -p 8080:8080 --shm-size="3g" --cpus=2.5 hentype/custom
```

run from hub.docker:
```
docker pull hentype/custom:latest
```

start Airflow:
```
airflow standalone
```