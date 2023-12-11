import os

import zerohertzLib as zz

SLACK = os.environ.get("SLACK")
KOR = bool(int(os.environ.get("KOR")))

if __name__ == "__main__":
    try:
        slack = zz.api.SlackBot(
            SLACK,
            channel="zerohertz",
            name="Stock",
            icon_emoji="chart_with_upwards_trend",
        )
        balance = zz.quant.Balance(path="stock", kor=KOR)
        path = balance.table()
        slack.file(path)
    except Exception as e:
        slack.message(
            ":warning:" * 3
            + "ERROR!!!"
            + ":warning:" * 3
            + "\n"
            + "```\n"
            + str(e)
            + "\n```",
        )
