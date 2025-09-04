FROM python:3.11

LABEL maintainer="Zerohertz <ohg3417@gmail.com>"
LABEL description="Airflow: JMY"
LABEL license="MIT"

ARG API_URI
ARG ADMIN_EMAIL
ARG ADMIN_PASSWORD

WORKDIR /app
COPY main.py .

RUN pip install --no-cache-dir \
    requests \
    pandas \
    xlrd \
    loguru

CMD ["python3", "main.py"]
