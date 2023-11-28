import os
import time

import pandas as pd
import zerohertzLib as zz
from prettytable import PrettyTable
from selenium import webdriver

# DISCORD WEBHOOK
WEBHOOK = os.environ.get("WEBHOOK")


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


def main(discord, browser, target):
    discord.message("# :chart_with_upwards_trend: STOCK")
    table = PrettyTable()
    table.field_names = [
        "NAME",
        "Purchase Price",
        "Current Price",
        "Quantity",
        "Profit and Loss (P&L)",
    ]
    TOTAL_BUY = TOTAL_EARN = 0
    for idx, tar in target.iterrows():
        stock_name, price = get_price(browser, tar["Name"])
        if tar["Name"] != stock_name:
            discord.message(
                f"Index: {idx}\nstock_name: {stock_name}\ntar['Name']: {tar['Name']}"
            )
        total = (price - tar["Buy"]) * tar["Quantity"]
        table.add_row(
            [
                stock_name,
                f"{tar['Buy']:,.0f}",
                f"{price:,.0f}",
                f"{tar['Quantity']:,.0f}",
                f"{total:,.0f}",
            ]
        )
        TOTAL_BUY += tar["Buy"] * tar["Quantity"]
        TOTAL_EARN += total
    table.add_row(["TOTAL", f"{TOTAL_BUY:,.0f}", "-", "-", f"{TOTAL_EARN:,.0f}"])
    discord.message(str(table), codeblock=True)


if __name__ == "__main__":
    df = pd.read_excel("data/Stock.xlsx")
    target = target_data(df)
    Discord = zz.api.Discord(WEBHOOK)
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
        main(Discord, browser, target)

    except Exception as e:
        Discord.message(":warning:" * 10 + "ERROR!!!" + ":warning:" * 10)
        Discord.message(str(e), codeblock=True)
