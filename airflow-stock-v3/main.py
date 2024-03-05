import os
import time
import traceback
from datetime import datetime, timedelta

import FinanceDataReader as fdr
import pytz
import zerohertzLib as zz
from matplotlib import pyplot as plt
from matplotlib import ticker

SLACK = os.environ.get("SLACK")


def _exchange():
    now = datetime.now()
    data = fdr.DataReader("USD/KRW", now - timedelta(days=1))
    return data.Close[-1]


def _merge(balance_1, balance_2, exchange=None):
    if exchange:
        for key, value in balance_2.items():
            balance_2.balance["stock"][key][1] = value[1] * exchange
            balance_2.balance["stock"][key][2] = value[2] * exchange
            balance_2.balance["stock"][key][-1] = value[-1] * exchange
        balance_2.balance["cash"] = balance_2.balance["cash"] * exchange
    balance_1.balance["stock"] = dict(list(balance_1.items()) + list(balance_2.items()))
    balance_1.balance["cash"] += balance_2.balance["cash"]
    return balance_1


def _balance():
    exchange = _exchange()
    try:
        balance = zz.quant.Balance(path="stock/ISA")
    except KeyError:
        balance = None
    if balance is None:
        balance = zz.quant.Balance(path="stock/NORMAL")
    else:
        balance = _merge(balance, zz.quant.Balance(path="stock/NORMAL"))
    balance = _merge(
        balance, zz.quant.Balance(path="stock/NORMAL", kor=False), exchange
    )
    balance.balance["stock"] = dict(
        sorted(
            balance.balance["stock"].items(),
            key=lambda item: item[1][1] * item[1][3],
            reverse=True,
        )
    )
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
    data_bar = {}
    for key, value in data[-1]["stock"].items():
        data_bar[key] = value[5]
    zz.plot.figure((20, 10))
    zz.plot.barv(
        data_bar,
        xlab="",
        ylab=f"Profit and Loss (P&L) [₩]",
        title="",
        rot=45,
        per=False,
        save=False,
    )
    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    path_bar = zz.plot.savefig("bar", 100)
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
