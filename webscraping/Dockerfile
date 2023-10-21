# docker build -t hentype/standalone-chrome-airflow .
# docker run -dit -p 4444:4444 -p 8080:8080 --shm-size="3g" --cpus=2.5 hentype/standalone-chrome-airflow

FROM selenium/standalone-chrome:latest

RUN sudo apt update
RUN sudo apt-get -y install python3-pip
RUN sudo pip3 install selenium
RUN sudo pip3 install PyGithub

ENV SE_VNC_NO_PASSWORD=1
ENV SE_NODE_MAX_SESSIONS=5
ENV SE_NODE_SESSION_TIMEOUT=15

EXPOSE 4444
EXPOSE 8080

USER root

RUN sudo apt-get install -y curl wget git

RUN sudo git clone -b dev https://github.com/cristian-encalada/Alquivago.git /root/Alquivago

# instalar Apache Airflow 
ENV AIRFLOW_HOME=/root/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=false
ENV AIRFLOW_VERSION=2.7.1
ENV PYTHON_VERSION=3.8
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
RUN sudo pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

RUN mkdir -p /root/airflow/dags && \
    cd /root/airflow/dags && \
    git clone -b dev https://github.com/cristian-encalada/Alquivago.git /root/airflow/dags && \
    mkdir /root/airflow/tmp && \
    cp /root/airflow/dags/webscraping/webscraping_dags/*.py /root/airflow/tmp && \
    rm -r /root/airflow/dags &&\
    mkdir /root/airflow/dags &&\
    cp /root/airflow/tmp/*.py /root/airflow/dags &&\
    rm -r /root/airflow/tmp

# CMD airflow standalone