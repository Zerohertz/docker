FROM python:3.8

ENV GRADIO_SERVER_PORT=7860

WORKDIR /app

RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx

COPY ./src/gradio/requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src/gradio/main.py /app/
CMD ["python", "main.py"]