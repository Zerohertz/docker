FROM python:3.8

WORKDIR /app
COPY main.py .

COPY requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
