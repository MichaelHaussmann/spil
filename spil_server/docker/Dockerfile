# Must be built from spils' repo root folder
# Build:                docker build -t spil/spil -f spil_server/docker/Dockerfile .
# Run with python:      docker run -ti spil/spil python

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./spil_server/docker/requirements.txt /spil/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /spil/requirements.txt

# spil will contain spil
COPY ./spil  /spil/spil

# This is a placeholder for a later custom config (see docker-compose.yml)
RUN mkdir /spil_conf
ENV PYTHONPATH="${PYTHONPATH}:/spil:/spil_conf"

# spil_hamlet_conf contains the spil demo config
COPY ./spil_hamlet_conf /spil/spil_hamlet_conf

# App will contain the fastapi app
# Starting app:main.py is already included in the base docker image (tiangolo/uvicorn-gunicorn-fastapi)
COPY ./spil_server/fastapi/app /app