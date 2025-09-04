import os
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import requests
from loguru import logger

API_URI = os.environ.get("API_URI")
ADMIN_DATA = {
    "grant_type": "password",
    "username": os.environ.get("ADMIN_EMAIL"),
    "password": os.environ.get("ADMIN_PASSWORD"),
}


def download_data():
    logger.info("Download data: Start")
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    ymd = now.strftime("%Y%m%d")
    file_name = f"병역지정업체검색_{ymd}.xls"
    url = "https://work.mma.go.kr/caisBYIS/search/downloadBYJJEopCheExcel.do"
    data = {"eopjong_gbcd": "2", "al_eopjong_gbcd": "", "eopjong_gbcd_list": ""}
    response = requests.post(url, data=data)
    with open(file_name, "wb") as file:
        file.write(response.content)
    logger.info("Download data: End")
    return file_name


def login():
    response = requests.post(f"{API_URI}/v1/auth/password/token", data=ADMIN_DATA)
    logger.info(f"Log In: {response.status_code=}")
    data = response.json()
    if response.status_code != 200:
        logger.critical(data)
    return data["access_token"]


def _create(token, date, data):
    response = requests.post(
        f"{API_URI}/v1/jmy",
        headers={"Authorization": f"Bearer {token}"},
        json=dict(
            name=data["업체명"],
            year=data["선정년도"],
            location=data["지방청"],
            address=data["주소"],
            type_=data["업종"],
            size=data["기업규모"],
            research=data["연구분야"],
            date=f"{date[:4]}-{date[4:6]}-{date[6:]}",
            b_assigned=data["보충역 배정인원"],
            b_new=data["보충역 편입인원"],
            b_old=data["보충역 복무인원"],
            a_assigned=data["현역 배정인원"],
            a_new=data["현역 편입인원"],
            a_old=data["현역 복무인원"],
        ),
    )
    data = response.json()
    if response.status_code != 200:
        logger.critical(data)


def create(token, file):
    date = file.split(".")[0].split("_")[1]
    data = pd.read_excel(file)
    for index, row in data.iterrows():
        _create(
            token=token, date=date, data=row.where(pd.notnull(row), "None").to_dict()
        )


def main():
    file = download_data()
    token = login()
    create(token=token, file=file)


if __name__ == "__main__":
    main()
