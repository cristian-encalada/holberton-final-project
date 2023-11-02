run in local:
```
docker build -t hentype/standalone-chrome-airflow .
docker run -dit -p 4444:4444 -p 8080:8080 --shm-size="3g" --cpus=2.5 hentype/standalone-chrome-airflow
```

run from hub.docker:
```
docker pull hentype/standalone-chrome-airflow
```

* configure environment variable for a GitHub token on your system:
```
root@0d545fdeaefb:/# export TOKEN=githubtoken
```

start Airflow:
```
root@0d545fdeaefb:/# airflow standalone
```