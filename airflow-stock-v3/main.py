import os
import time
import traceback
from collections import defaultdict
from datetime import datetime

import pytz
import zerohertzLib as zz

NORMAL = os.environ.get("NORMAL")
ISA = os.environ.get("ISA")
SLACK = os.environ.get("SLACK")


def _balance():
    reports = defaultdict(list)
    isa_kor = zz.quant.Balance(ISA, path="stock/ISA")
    reports[":kr: `ISA   `"].append(f"""{isa_kor.balance.get("cash"):,.0f} [₩]""")
    nor_kor = zz.quant.Balance(NORMAL, path="stock/NORMAL")
    reports[":kr: `NORMAL`"].append(f"""{nor_kor.balance.get("cash"):,.0f} [₩]""")
    isa_kor.merge(nor_kor)
    nor_ovs = zz.quant.Balance(NORMAL, path="stock/NORMAL", kor=False)
    exchange = nor_ovs._exchange()
    reports[":us: `NORMAL`"].append(
        f"""{nor_ovs.balance.get("cash") * exchange:,.0f} [₩]"""
    )
    reports[":us: `NORMAL`"].append(f"""{nor_ovs.balance.get("cash"):,.0f} [$]""")
    reports[":us: `NORMAL`"].append(f"{exchange:,.0f} [₩/$]")
    isa_kor.merge(nor_ovs)
    return isa_kor, reports


def make_messages(reports):
    messages = []
    max_value_length = max(len(value[0]) for value in reports.values())
    for key, values in reports.items():
        adjusted_value = values[0].rjust(max_value_length)
        if len(values) == 1:
            messages.append(f"{key}:`{adjusted_value}`")
        else:
            messages.append(f"{key}:`{adjusted_value}`\t(`{values[1]}`, `{values[2]}`)")
    return "\n".join(messages)


def main(slack):
    try:
        data = zz.util.Json("stock/balance.json").data
    except:
        data = []
    korea_time_zone = pytz.timezone("Asia/Seoul")
    now = datetime.now(korea_time_zone)
    balance, reports = _balance()
    data.append(balance.balance)
    data[-1]["time"] = str(now)
    zz.util.write_json(data, "stock/balance")
    path_bar = balance.barv()
    path_balance, path_portfolio = balance.table(), balance.pie()
    if path_balance is None:
        slack.message("Balance: NULL", True)
    else:
        cash = balance.balance.get("cash")
        reports[":money_with_wings: `TOTAL `"].append(f"{cash:,.0f} [₩]")
        response = slack.message(make_messages(reports))
        thread_ts = response.get("ts")
        time.sleep(3)
        slack.file(path_bar, thread_ts)
        time.sleep(3)
        slack.file(path_balance, thread_ts)
        time.sleep(3)
        slack.file(path_portfolio, thread_ts)


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
        slack.message(traceback.format_exc(), True, response.get("ts"))
