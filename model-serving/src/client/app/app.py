from fastapi import FastAPI
from main import main
from pydantic import BaseModel

app = FastAPI()


class RequestModel(BaseModel):
    file_id: str


@app.post("/")
def inference(request: RequestModel):
    pt, labels = main(request.file_id)
    return {
        "request_info": {"file_id": request.file_id, "process_time": pt},
        "labels": [
            labels,
        ],
    }
