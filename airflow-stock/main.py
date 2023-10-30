import json
import os
import time

import requests
from prettytable import PrettyTable
from selenium import webdriver

# DISCORD WEBHOOK
WEBHOOK = os.environ.get("WEBHOOK")
# 주식 구매 정보
STOCK = eval(os.environ.get("STOCK"))
print(STOCK)


def get_price(browser, CODE):
    browser.get(f"https://finance.naver.com/item/main.naver?code={CODE}")
    element = browser.find_element(
        "xpath",
        "/html/body/div[3]/div[2]/div[2]/div[1]/div[5]/table/tbody/tr[1]/td[1]",
    )
    return int(element.text.replace(",", ""))


def send_discord_message(webhook_url, content):
    data = {"content": content}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    return response


def send_discord_messages(webhook_url, contents):
    headers = {"Content-Type": "application/json"}
    for content in contents:
        data = {"content": content}
        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        time.sleep(1)
    return response


if __name__ == "__main__":
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
        messages = [f"# :chart_with_upwards_trend: STOCK\n"]
        table = PrettyTable()
        table.field_names = [
            "COMPANY NAME",
            "Purchase Price",
            "Current Price",
            "Quantity",
            "Profit and Loss (P&L)",
        ]
        TOTAL_BUY = 0
        TOTAL_EARN = 0
        for COMPANY, CODE, PRICE, QUANTITY in STOCK:
            if len(str(table)) > 1500:
                messages.append("```\n" + str(table) + "\n```")
                table = PrettyTable()
                table.field_names = [
                    "COMPANY NAME",
                    "Purchase Price",
                    "Current Price",
                    "Quantity",
                    "Profit and Loss (P&L)",
                ]
            tmp = get_price(browser, CODE)
            total = (tmp - PRICE) * QUANTITY
            table.add_row([COMPANY, f"{PRICE:,}", f"{tmp:,}", QUANTITY, f"{total:,}"])
            TOTAL_BUY += PRICE * QUANTITY
            TOTAL_EARN += total
        else:
            table.add_row(["TOTAL", f"{TOTAL_BUY:,}", "-", "-", f"{TOTAL_EARN:,}"])
            messages.append("```\n" + str(table) + "\n```")
        send_discord_messages(WEBHOOK, messages)

    except Exception as e:
        send_discord_message(
            WEBHOOK,
            ":warning:" * 10
            + "ERROR!!!"
            + ":warning:" * 10
            + "\n"
            + "```\n"
            + str(e)
            + "\n```",
        )
