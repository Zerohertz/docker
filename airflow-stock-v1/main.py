import os
import time

import pandas as pd
import zerohertzLib as zz
from selenium import webdriver

SLACK = os.environ.get("SLACK")


def target_data(data):
    return data[~data["Buy"].isna() & data["Sell"].isna()]


def get_price(browser, name):
    browser.get(
        f"https://stock.mk.co.kr/search/list?search_string={name.replace(' ', '+')}"
    )
    time.sleep(3)
    stock_name = browser.find_element(
        "xpath",
        "/html/body/div/main/main/section/div[2]/div/div/div[1]/section/div/div/div/table/tbody/tr/td[1]/span",
    ).text
    price = int(
        browser.find_element(
            "xpath",
            "/html/body/div/main/main/section/div[2]/div/div/div[1]/section/div/div/div/table/tbody/tr/td[2]/span",
        ).text.replace(",", "")
    )
    return stock_name, price


def main(slack, browser, target):
    col = [
        "Purchase Price",
        "Current Price",
        "Quantity",
        "Profit and Loss (P&L)",
    ]
    row = []
    data = []
    TOTAL_BUY = TOTAL_EARN = 0
    for idx, tar in target.iterrows():
        stock_name, price = get_price(browser, tar["Name"])
        if tar["Name"] != stock_name:
            slack.message(
                f"Index: {idx}\nstock_name: {stock_name}\ntar['Name']: {tar['Name']}"
            )
        total = (price - tar["Buy"]) * tar["Quantity"]
        row.append(stock_name)
        data.append(
            [
                f"{tar['Buy']:,.0f}",
                f"{price:,.0f}",
                f"{tar['Quantity']:,.0f}",
                f"{total:,.0f}",
            ]
        )
        TOTAL_BUY += tar["Buy"] * tar["Quantity"]
        TOTAL_EARN += total
    row.append("TOTAL")
    data.append([f"{TOTAL_BUY:,.0f}", "-", "-", f"{TOTAL_EARN:,.0f}"])
    path = zz.plot.table(data, col, row, title="Stock")
    slack.file(path)


if __name__ == "__main__":
    df = pd.read_excel("data/Stock.xlsx")
    target = target_data(df)
    slack = zz.api.SlackBot(
        SLACK, "zerohertz", name="Stock", icon_emoji="chart_with_upwards_trend"
    )
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        )
        browser = webdriver.Chrome(options)
        main(slack, browser, target)

    except Exception as e:
        slack.message(":warning:" * 10 + "ERROR!!!" + ":warning:" * 10)
        slack.message(str(e), codeblock=True)
