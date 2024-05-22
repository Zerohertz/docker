FROM python:3.11

WORKDIR /app
COPY main.py .

RUN pip install --no-cache-dir zerohertzLib[quant]==1.0.9

CMD ["python3", "main.py"]
