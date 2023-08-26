import os
import json

from skimage import io


def yolo2ls(home):
    '''
    home: path (str)
    ├── test
    │   └── labels
    ├── train
    │   └── labels
    └── val
        └── labels
    '''
    tmp = os.getcwd()
    os.chdir(home)
    for status in ["train", "val", "test"]:
        res = []
        os.chdir(home)
        os.chdir(status)
        for i in os.listdir():
            if ".png" in i:
                #----------- JSON -----------#
                obj = {"data": {"image": f"/data/local-files/?d={status}/{i}"}}
                #----------- IMG META -----------#
                img = io.imread(i)
                original_height, original_width, c = img.shape
                #----------- Pre-labeling -----------#
                gtf = "labels/" + i.replace("png", "txt")
                with open(gtf, "r") as f:
                    gt = f.readlines()
                result_list = []
                for j in gt:
                    cx, cy, w, h = [float(k) for k in j.strip().split(" ")[1:]]
                    xmin = max(0.0, round(100.0 * (cx - w / 2), 2))
                    ymin = max(0.0, round(100.0 * (cy - h / 2)))
                    xmax = min(100.0, round(100.0 * (cx + w / 2)))
                    ymax = min(100.0, round(100.0 * (cy + h / 2)))
                    points = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]
                    result_list.append(
                            {"original_width": original_width,
                            "original_height": original_height,
                            "image_rotation": 0,
                            "value": {
                                "points": points,
                                "closed": True,
                                "polygonlabels": ["receipt"]
                            },
                            "from_name": "label",
                            "to_name": "image",
                            "type": "polygonlabels",
                            "origin": "manual"}
                        )
                pred = [{
                    "result": result_list
                }]
                obj.update({"annotations": pred})
                res.append(obj)
        os.chdir(tmp)
        with open(f"./pre-labeling-{status}.json", "w") as f:
            json.dump(res, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    home = ${home}
    yolo2ls(home)
