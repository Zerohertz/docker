import os

import zerohertzLib as zz

SLACK = os.environ.get("SLACK")
START_DAY = os.environ.get("START_DAY")
MP_NUM = int(os.environ.get("MP_NUM"))
KOR = bool(int(os.environ.get("KOR")))

if __name__ == "__main__":
    try:
        qsb = zz.quant.QuantSlackBotKI(
            [],
            token=SLACK,
            channel="zerohertz",
            start_day=START_DAY,
            path="stock",
            name="Stock",
            icon_emoji="chart_with_upwards_trend",
            mp_num=MP_NUM,
            kor=KOR,
        )
        qsb.sell()
    except Exception as e:
        qsb.message(
            ":warning:" * 3
            + "ERROR!!!"
            + ":warning:" * 3
            + "\n"
            + "```\n"
            + str(e)
            + "\n```",
        )
