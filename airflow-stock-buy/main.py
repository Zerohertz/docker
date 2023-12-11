import os

import zerohertzLib as zz

SYMBOLS = int(os.environ.get("SYMBOLS"))
SLACK = os.environ.get("SLACK")
START_DAY = os.environ.get("START_DAY")
TOP = int(os.environ.get("TOP"))
MP_NUM = int(os.environ.get("MP_NUM"))
KOR = bool(int(os.environ.get("KOR")))

if __name__ == "__main__":
    try:
        if KOR:
            channel = "stock_kor_buy"
        else:
            channel = "stock_ovs_buy"
        qsb = zz.quant.QuantSlackBotFDR(
            SYMBOLS,
            token=SLACK,
            channel=channel,
            start_day=START_DAY,
            top=TOP,
            name="Buy",
            icon_emoji="chart_with_upwards_trend",
            mp_num=MP_NUM,
            kor=KOR,
        )
        qsb.buy()
        if KOR:
            qsb = zz.quant.QuantSlackBotFDR(
                ["069500", "226980", "114800", "251340", "252670"],
                token=SLACK,
                channel=channel,
                start_day=START_DAY,
                top=TOP,
                name="Index",
                icon_emoji="chart_with_upwards_trend",
                mp_num=MP_NUM,
                kor=KOR,
            )
            qsb.index()
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
