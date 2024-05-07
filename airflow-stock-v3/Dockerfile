FROM python:3.8

WORKDIR /app
COPY main.py .

RUN pip install --no-cache-dir \
    pytz \
    zerohertzLib[quant]==1.0.7

CMD ["python3", "main.py"]
