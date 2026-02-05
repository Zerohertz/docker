import os
import traceback
from datetime import datetime

import zerohertzLib as zz
from matplotlib import pyplot as plt
from matplotlib import ticker

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_BOT_CHANNEL = os.environ.get("DISCORD_BOT_CHANNEL")


def main(discord):
    try:
        data = zz.util.Json("stock/balance.json").data
    except FileNotFoundError:
        discord.message("Balance: NULL", "bash")
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
    zz.plot.figure((30, 15))
    zz.plot.plot(
        xdata,
        ydata,
        xlab="",
        ylab="Asset [₩]",
        stacked=True,
        title="",
        colors="Set2",
        markersize=0,
    )
    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    plt.legend(
        loc="upper left",
        bbox_to_anchor=(1, 1.02),
        ncol=len(stocks) // 30 + 1,
        fontsize="small",
    )
    path_time = zz.plot.savefig("time", 100)
    discord.file(path_time)
    return None


if __name__ == "__main__":
    discord = zz.api.DiscordBot(DISCORD_BOT_TOKEN, DISCORD_BOT_CHANNEL)
    try:
        zz.plot.font(kor=True)
        main(discord)
    except Exception as exc:
        exc_str = str(exc)
        response = discord.message(
            ":warning:" * 3
            + "\tERROR!!!\t"
            + ":warning:" * 3
            + "\n"
            + "```\n"
            + exc_str
            + "\n```",
        )
        thread_id = discord.get_thread_id(response, name=exc_str)
        discord.message(traceback.format_exc(), "python", thread_id)
