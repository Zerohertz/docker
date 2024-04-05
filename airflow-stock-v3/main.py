import os
import time
import traceback
from datetime import datetime

import pytz
import zerohertzLib as zz

SLACK = os.environ.get("SLACK")
NORMAL = os.environ.get("NORMAL")
ISA = os.environ.get("ISA")


def _balance():
    try:
        balance = zz.quant.Balance(ISA, path="stock/ISA")
    except KeyError:
        balance = None
    if balance is None:
        balance = zz.quant.Balance(NORMAL, path="stock/NORMAL")
    else:
        balance.merge(zz.quant.Balance(NORMAL, path="stock/NORMAL"))
    balance.merge(zz.quant.Balance(NORMAL, path="stock/NORMAL", kor=False))
    return balance


def main(slack):
    try:
        data = zz.util.Json("stock/balance.json").data
    except:
        data = []
    korea_time_zone = pytz.timezone("Asia/Seoul")
    now = datetime.now(korea_time_zone)
    balance = _balance()
    data.append(balance.balance)
    data[-1]["time"] = str(now)
    zz.util.write_json(data, "stock/balance")
    path_bar = balance.barv()
    path_balance, path_portfolio = balance.table(), balance.pie()
    if path_balance is None:
        slack.message("Balance: NULL", True)
    else:
        response = slack.file(path_bar)
        thread_ts = list(response.json()["file"]["shares"]["private"].values())[0][0][
            "ts"
        ]
        time.sleep(3)
        slack.file(path_balance, thread_ts)
        time.sleep(3)
        slack.file(
            path_portfolio,
            thread_ts,
        )


if __name__ == "__main__":
    slack = zz.api.SlackBot(
        SLACK,
        channel="stock_balance",
        name="Balance",
        icon_emoji="moneybag",
        timeout=30,
    )
    try:
        zz.plot.font(kor=True)
        main(slack)
    except Exception as e:
        response = slack.message(
            ":warning:" * 3
            + "\tERROR!!!\t"
            + ":warning:" * 3
            + "\n"
            + "```\n"
            + str(e)
            + "\n```",
        )
        slack.message(traceback.format_exc(), True, response.json()["ts"])
