
FROM apache/airflow:3.3.2

USER root
RUN mkdir -p /opt/airflow/project && chown -R airflow:0 /opt/airflow/project

USER airflow
RUN pip install --no-cache-dir pandas requests

ENV PYTHONPATH="/opt/airflow/project"

WORKDIR /opt/airflow/project
