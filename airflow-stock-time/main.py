import os
import traceback
from datetime import datetime

import zerohertzLib as zz
from matplotlib import pyplot as plt
from matplotlib import ticker

SLACK = os.environ.get("SLACK")
KOR = bool(int(os.environ.get("KOR")))


def main(slack, data_path, dim):
    try:
        data = zz.util.Json(f"{data_path}.json").data
    except FileNotFoundError:
        slack.message("Balance: NULL", True)
        return None
    fmt = "%Y-%m-%d %H:%M:%S.%f%z"
    xdata, stocks = [], []
    for data_ in data:
        xdata.append(datetime.strptime(data_["time"], fmt))
        for stock in data_["stock"].keys():
            if stock not in stocks:
                stocks.append(stock)
    ydata = {}
    for stock in stocks:
        ydata[stock] = [0 for _ in range(len(xdata))]
    ydata["Total"] = [0 for _ in range(len(xdata))]
    for idx, data_ in enumerate(data):
        for key, value in data_["stock"].items():
            ydata[key][idx] = value[2] * value[3]
        ydata["Total"][idx] = data_["cash"]
    zz.plot.figure((20, 10))
    zz.plot.plot(
        xdata,
        ydata,
        xlab="",
        ylab=f"Asset [{dim}]",
        stacked=True,
        title="",
        markersize=6,
        save=False,
    )
    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1.02))
    path_time = zz.plot.savefig("time", 100)
    slack.file(path_time)
    return None


if __name__ == "__main__":
    try:
        if KOR:
            channel = "stock_kor_time"
            data_path = "stock/stock-kor"
            dim = "￦"
        else:
            channel = "stock_ovs_time"
            data_path = "stock/stock-ovs"
            dim = "$"
        slack = zz.api.SlackBot(
            SLACK,
            channel=channel,
            name="Balance",
            icon_emoji="moneybag",
        )
        main(slack, data_path, dim)
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