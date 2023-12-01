FROM python:3.8

WORKDIR /app
COPY main.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
