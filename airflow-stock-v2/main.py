import os

import zerohertzLib as zz

SLACK = os.environ.get("SLACK")
KOR = bool(int(os.environ.get("KOR")))

if __name__ == "__main__":
    try:
        if KOR:
            channel = "stock_kor_balance"
        else:
            channel = "stock_ovs_balance"
        slack = zz.api.SlackBot(
            SLACK,
            channel=channel,
            name="Balance",
            icon_emoji="moneybag",
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
