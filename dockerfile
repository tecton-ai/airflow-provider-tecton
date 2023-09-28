# docker build -t tecton_provider .
# docker run -v /path/to/airflowconfigs/airflow:/root/airflow -p 8080:8080 tecton_provider
FROM python:3.9-slim

RUN apt-get update \
&& apt-get install gcc python3-dev vim -y \
&& apt-get clean

RUN mkdir -p /opt/tecton_provider/
WORKDIR /opt/tecton_provider/

RUN pip install pandas
RUN pip install pyarrow
RUN pip install fastparquet

RUN pip install --no-cache-dir --upgrade pip && \
	pip install --no-cache-dir apache-airflow>=2.0


COPY ./ /opt/tecton_provider

ENV PYTHONPATH "${PYTHONPATH}:/opt/tecton_provider"

ENV AIRFLOW_HOME=/root/airflow

CMD ["airflow", "standalone"]
