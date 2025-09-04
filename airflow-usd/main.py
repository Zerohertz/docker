import os
import time
import traceback
from datetime import datetime, timedelta

import FinanceDataReader as fdr
import zerohertzLib as zz

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_BOT_CHANNEL = os.environ.get("DISCORD_BOT_CHANNEL")


if __name__ == "__main__":
    discord = zz.api.DiscordBot(DISCORD_BOT_TOKEN, DISCORD_BOT_CHANNEL)
    try:
        zz.plot.font(kor=True)
        now = datetime.now()
        start_day = now - timedelta(days=365)
        start_day = start_day.strftime("%Y%m%d")
        data = fdr.DataReader("USD/KRW", start_day)
        raw = data.Close
        ma20 = raw.rolling(20).mean()
        path = zz.plot.plot(
            data.index,
            {"RAW": raw, "MA20": ma20},
            xlab="Time",
            ylab="Won [₩]",
            title="USD/KRW",
            markersize=6,
            figsize=(20, 10),
        )
        month_low = (raw[-1] - raw[-30:].min()) / raw[-30:].min() * 100
        month_mean = (raw[-1] - raw[-30:].mean()) / raw[-30:].mean() * 100
        year_low = (raw[-1] - raw.min()) / raw.min() * 100
        year_mean = (raw[-1] - raw.mean()) / raw.mean() * 100
        year_q1 = (raw[-1] - raw.quantile(0.25)) / raw.quantile(0.25) * 100
        message = f":money_with_wings: 현재 USD/KRW: {raw[-1]:.2f}₩\n"
        message += ":calendar: 최근 1달\n"
        message += f"\t:dollar: 평균 대비 현재 시세: {month_mean:.2f}%\n"
        message += f"\t:dollar: 저점 대비 현재 시세: {month_low:.2f}%\n"
        message += ":calendar: 최근 1년\n"
        message += f"\t:dollar: 평균 대비 현재 시세: {year_mean:.2f}%\n"
        message += f"\t:dollar: 저점 대비 현재 시세: {year_low:.2f}%\n"
        message += f"\t:dollar: Q1 대비 현재 시세: {year_q1:.2f}%\n"
        response = discord.message(message)
        response = discord.create_thread(message, response.json()["id"])
        time.sleep(3)
        discord.file(path, response.json()["id"])
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
        response = discord.create_thread(exc_str, response.json()["id"])
        discord.message(traceback.format_exc(), "python", response.json()["id"])
