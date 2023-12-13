import os
import traceback

import zerohertzLib as zz

SLACK = os.environ.get("SLACK")
START_DAY = os.environ.get("START_DAY")
TOP = int(os.environ.get("TOP"))
MP_NUM = int(os.environ.get("MP_NUM"))
KOR = bool(int(os.environ.get("KOR")))

if __name__ == "__main__":
    try:
        if KOR:
            channel = "stock_kor_sell"
        else:
            channel = "stock_ovs_sell"
        qsb = zz.quant.QuantSlackBotKI(
            [],
            start_day=START_DAY,
            top=TOP,
            token=SLACK,
            channel=channel,
            name="Sell",
            icon_emoji="chart_with_upwards_trend",
            mp_num=MP_NUM,
            kor=KOR,
            path="stock",
        )
        qsb.sell()
    except Exception as e:
        response = qsb.message(
            ":warning:" * 3
            + "\tERROR!!!\t"
            + ":warning:" * 3
            + "\n"
            + "```\n"
            + str(e)
            + "\n```",
        )
        qsb.message(traceback.format_exc(), True, response.json()["ts"])
