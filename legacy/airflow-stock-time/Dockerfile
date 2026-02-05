FROM python:3.12

LABEL maintainer="Zerohertz <ohg3417@gmail.com>"
LABEL description="Airflow: Stock Time"
LABEL license="MIT"

WORKDIR /app
COPY main.py .

RUN pip install --no-cache-dir zerohertzLib[quant]==1.2.3

CMD ["python3", "main.py"]
