FROM python:3.11

WORKDIR /app
COPY main.py .

RUN pip install --no-cache-dir \
    pytz \
    zerohertzLib[quant]==1.0.8

CMD ["python3", "main.py"]
