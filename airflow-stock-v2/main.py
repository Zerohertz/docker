import os
import traceback
from datetime import datetime

import pytz
import zerohertzLib as zz
from matplotlib import pyplot as plt
from matplotlib import ticker

SLACK = os.environ.get("SLACK")
KOR = bool(int(os.environ.get("KOR")))

if __name__ == "__main__":
    try:
        if KOR:
            channel = "stock_kor_balance"
            data_path = "stock/stock-kor"
            dim = "₩"
        else:
            channel = "stock_ovs_balance"
            data_path = "stock/stock-ovs"
            dim = "$"
        slack = zz.api.SlackBot(
            SLACK,
            channel=channel,
            name="Balance",
            icon_emoji="moneybag",
        )
        korea_time_zone = pytz.timezone("Asia/Seoul")
        now = datetime.now(korea_time_zone)
        try:
            data = zz.util.Json(f"{data_path}.json").data
        except:
            data = []
        balance = zz.quant.Balance(path="stock", kor=KOR)
        data.append(balance.balance)
        data[-1]["time"] = str(now)
        zz.util.write_json(data, data_path)
        data_bar = {}
        for key, value in data[-1]["stock"].items():
            data_bar[key] = value[5]
        zz.plot.figure((20, 10))
        zz.plot.barv(
            data_bar,
            xlab="",
            ylab=f"Profit and Loss (P&L) [{dim}]",
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
            thread_ts = list(response.json()["file"]["shares"]["private"].values())[0][
                0
            ]["ts"]
            slack.file(path_balance, thread_ts)
            slack.file(
                path_portfolio,
                thread_ts,
            )
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
