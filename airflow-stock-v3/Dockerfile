FROM python:3.11

WORKDIR /app
COPY main.py .

RUN pip install --no-cache-dir \
    pytz \
    zerohertzLib[quant]==1.1.3

CMD ["python3", "main.py"]
