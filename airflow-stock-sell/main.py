import os
import traceback
from datetime import datetime, timedelta

import FinanceDataReader as fdr
import zerohertzLib as zz

START_DAY = os.environ.get("START_DAY")
TOP = int(os.environ.get("TOP"))
SLACK = os.environ.get("SLACK")
MP_NUM = int(os.environ.get("MP_NUM"))
KOR = bool(int(os.environ.get("KOR")))
ACCOUNT = os.environ.get("ACCOUNT")


def main(channel, test_code):
    now = datetime.now()
    test_start_day = now - timedelta(days=30)
    test_data = fdr.DataReader(test_code, test_start_day)
    if KOR and test_data.index[-1].day != now.day:
        return False
    qsb = zz.quant.QuantSlackBotKI(
        ACCOUNT,
        start_day=START_DAY,
        ohlc="Close",
        top=TOP,
        token=SLACK,
        channel=channel,
        name="Sell",
        icon_emoji="chart_with_upwards_trend",
        mp_num=MP_NUM,
        kor=KOR,
        path=f"stock",
    )
    qsb.sell()
    return True


if __name__ == "__main__":
    if KOR:
        channel = "stock_kor_sell"
        code = "005930"
    else:
        channel = "stock_ovs_sell"
        code = "AAPL"
    slack = zz.api.SlackBot(SLACK, channel, name="Error", icon_emoji="warning")
    try:
        zz.plot.font(kor=True)
        if not main(channel, code):
            system = zz.api.SlackBot(SLACK, channel, name="System", icon_emoji="bank")
            system.message("> :zzz: 오늘은 휴장일 입니다. :zzz:")
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
