FROM selenium/standalone-chrome

USER root
RUN apt-get update \
    && apt-get install -y python3 python3-pip

WORKDIR /app
COPY main.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
