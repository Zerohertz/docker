import json
import math
import os

import cv2
import gradio as gr
import numpy as np
import requests

URL = "http://model-serving-client:80/"
INPUT_DIR = "/app/inputs"
OUTPUT_DIR = "/app/outputs"

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
}
OUTPUT_SIZE = 1200


def grid(grid_size, index):
    return (
        grid_size * (index // (OUTPUT_SIZE // grid_size)),
        grid_size * (index % (OUTPUT_SIZE // grid_size)),
    )


def resize(image, grid_size):
    h, w, _ = image.shape
    if h > w:
        new_height = grid_size
        new_width = int((w / h) * new_height)
    else:
        new_width = grid_size
        new_height = int((h / w) * new_width)
    resized_image = cv2.resize(image, (new_width, new_height))
    delta_w = grid_size - new_width
    delta_h = grid_size - new_height
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)
    return cv2.copyMakeBorder(
        resized_image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0]
    )


def vis_input(images):
    grid_size = math.ceil(math.sqrt(len(images)))
    grid_size = int(OUTPUT_SIZE / grid_size)
    palette = np.zeros((OUTPUT_SIZE, OUTPUT_SIZE, 3))
    img_list = []
    for idx, image in enumerate(images):
        img = cv2.imread(image.name)
        image_path = os.path.join(INPUT_DIR, image.name.split("/")[-1])
        img_list.append(image.name.split("/")[-1])
        x, y = grid(grid_size, idx)
        cv2.imwrite(image_path, img)
        palette[
            x : x + grid_size,
            y : y + grid_size,
            :,
        ] = resize(img, grid_size)
    palette = palette.astype("float32")
    palette = cv2.cvtColor(palette, cv2.COLOR_BGR2RGB)
    return palette / 255.0, img_list


def vis_output(images):
    grid_size = math.ceil(math.sqrt(len(images)))
    grid_size = int(OUTPUT_SIZE / grid_size)
    palette = np.zeros((OUTPUT_SIZE, OUTPUT_SIZE, 3))
    for idx, image in enumerate(images):
        img = cv2.imread(os.path.join(OUTPUT_DIR, image))
        x, y = grid(grid_size, idx)
        palette[
            x : x + grid_size,
            y : y + grid_size,
            :,
        ] = resize(img, grid_size)
    palette = palette.astype("float32")
    palette = cv2.cvtColor(palette, cv2.COLOR_BGR2RGB)
    return palette / 255.0


def DEMO(images):
    ORG, img_list = vis_input(images)
    CODE = []
    for query in img_list:
        DATA = {"file_id": query}
        response = requests.post(URL, headers=HEADERS, json=DATA)
        CODE.append(str(json.dumps(response.json(), indent=4)))
    RES = vis_output(img_list)
    CODE = "\n".join(CODE)
    return ORG, RES, CODE


inputs = [
    gr.Files(label="입력 이미지", file_types=["image"]),
]
outputs = [
    gr.Image(label="입력 이미지", type="numpy"),
    gr.Image(label="출력 이미지", type="numpy"),
    gr.Textbox(label="API 응답", text_align="left", show_copy_button=True),
]

iface = gr.Interface(
    fn=DEMO, inputs=inputs, outputs=outputs, title="DEMO", allow_flagging="never"
)

iface.launch(share=False, server_name="0.0.0.0")
