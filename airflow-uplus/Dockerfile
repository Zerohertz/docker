FROM selenium/standalone-chrome

USER root
RUN apt-get update \
    && apt-get install -y python3 python3-pip

RUN pip install requests

COPY main.py /app/main.py

WORKDIR /app

RUN pip3 install selenium

CMD ["python3", "main.py"]