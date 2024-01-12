FROM python:3.8

WORKDIR /app
COPY main.py .

RUN pip install --no-cache-dir zerohertzLib[quant]==0.7.8

CMD ["python3", "main.py"]