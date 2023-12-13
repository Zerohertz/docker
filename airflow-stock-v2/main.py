import os
import traceback

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
        if path is None:
            slack.message("Balance: NULL", True)
        else:
            slack.file(path)
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
