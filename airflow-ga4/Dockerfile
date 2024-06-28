FROM python:3.11

LABEL maintainer="Zerohertz <ohg3417@gmail.com>"
LABEL description="Airflow: Google Analytics 4"
LABEL license="MIT"

WORKDIR /app
COPY main.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
