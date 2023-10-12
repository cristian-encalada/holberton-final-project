# docker build -t hentype/custom .
# docker run -dit -p 4444:4444 -p 7900:7900 -p 8080:8080 --shm-size="2g" --cpus 1.5 hentype/custom 

FROM selenium/standalone-chrome:latest

RUN sudo apt update
RUN sudo apt-get -y install python3-pip
RUN sudo pip3 install selenium
RUN sudo pip install selenium

ENV SE_VNC_NO_PASSWORD=1
# ENV SE_VNC_VIEW_ONLY=1
ENV SE_NODE_MAX_SESSIONS=2
ENV SE_NODE_SESSION_TIMEOUT=10
ENV SE_VNC_NO_PASSWORD=1

EXPOSE 4444
EXPOSE 4443
EXPOSE 8080

USER root

RUN sudo apt-get install -y curl wget git

WORKDIR /root

RUN sudo git clone -b dev https://github.com/cristian-encalada/Alquivago.git

# instalar Apache Airflow 
ENV AIRFLOW_HOME=/root/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=false
ENV AIRFLOW_VERSION=2.7.1
ENV PYTHON_VERSION=3.8
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
RUN sudo pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# inicializa la base de datos de Airflow
RUN airflow db init

RUN mkdir -p /root/airflow/dags && \
    cd /root/airflow/dags && \
    git clone -b dev https://github.com/cristian-encalada/Alquivago.git /root/airflow/dags && \
    mkdir /root/airflow/tmp && \
    cp /root/airflow/dags/webscraping/webscraping_dags/*.py /root/airflow/tmp && \
    rm -r /root/airflow/dags &&\
    mkdir /root/airflow/dags &&\
    cp /root/airflow/tmp/*.py /root/airflow/dags &&\
    rm -r /root/airflow/tmp 
 
WORKDIR /root

# CMD airflow standalone