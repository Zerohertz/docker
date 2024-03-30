FROM selenium/standalone-chrome

USER root
RUN apt-get update \
    && apt-get install -y python3 python3-pip

RUN pip install zerohertzLib[api]==0.9.9
RUN pip install selenium

COPY main.py /app/main.py

WORKDIR /app

CMD ["python3", "main.py"]
