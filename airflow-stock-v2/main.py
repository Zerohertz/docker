import os

import zerohertzLib as zz

SLACK = os.environ.get("SLACK")

if __name__ == "__main__":
    qsb = zz.quant.QuantSlackBotKI(
        [],
        token=SLACK,
        channel="zerohertz",
        start_day="20200101",
        path="stock",
        name="Stock",
        icon_emoji="chart_with_upwards_trend",
        mp_num=6,
        analysis=True,
    )
    qsb.sell()
