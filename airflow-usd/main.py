import os
import time
import traceback
from datetime import datetime, timedelta

import FinanceDataReader as fdr
import zerohertzLib as zz

SLACK = os.environ.get("SLACK")


if __name__ == "__main__":
    slack = zz.api.SlackBot(
        SLACK,
        channel="usd",
        name="USD/KRW",
        icon_emoji="dollar",
        timeout=30,
    )
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
        message += f":calendar: 최근 1달\n"
        message += f"\t:dollar: 평균 대비 현재 시세: {month_mean:.2f}%\n"
        message += f"\t:dollar: 저점 대비 현재 시세: {month_low:.2f}%\n"
        message += f":calendar: 최근 1년\n"
        message += f"\t:dollar: 평균 대비 현재 시세: {year_mean:.2f}%\n"
        message += f"\t:dollar: 저점 대비 현재 시세: {year_low:.2f}%\n"
        message += f"\t:dollar: Q1 대비 현재 시세: {year_q1:.2f}%\n"
        response = slack.message(message)
        time.sleep(3)
        slack.file(path, response.get("ts"))
    except Exception as error:
        response = slack.message(
            ":warning:" * 3
            + "\tERROR!!!\t"
            + ":warning:" * 3
            + "\n"
            + "```\n"
            + str(error)
            + "\n```",
        )
        slack.message(traceback.format_exc(), True, response.get("ts"))
