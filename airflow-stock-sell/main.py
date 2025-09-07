import os
import traceback
from datetime import datetime, timedelta

import FinanceDataReader as fdr
import zerohertzLib as zz

NORMAL = os.environ.get("NORMAL")
ISA = os.environ.get("ISA")
START_DAY = os.environ.get("START_DAY")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_BOT_CHANNEL = os.environ.get("DISCORD_BOT_CHANNEL")
MP_NUM = int(os.environ.get("MP_NUM"))
KOR = bool(int(os.environ.get("KOR")))


def main(test_code):
    now = datetime.now()
    test_start_day = now - timedelta(days=30)
    test_data = fdr.DataReader(test_code, test_start_day)
    if KOR and test_data.index[-1].day != now.day:
        return False
    if KOR:
        ACCOUNT = {"NORMAL": NORMAL, "ISA": ISA}
    else:
        ACCOUNT = {"NORMAL": NORMAL}
    for name, account in ACCOUNT.items():
        qbki = zz.quant.QuantBotKI(
            account,
            start_day=START_DAY,
            ohlc="Close",
            token=DISCORD_BOT_TOKEN,
            channel=DISCORD_BOT_CHANNEL,
            name="Sell",
            mp_num=MP_NUM,
            kor=KOR,
            path=f"stock/{name}",
        )
        qbki.sell()
    return True


if __name__ == "__main__":
    if KOR:
        code = "005930"
    else:
        code = "AAPL"
    discord = zz.api.DiscordBot(token=DISCORD_BOT_TOKEN, channel=DISCORD_BOT_CHANNEL)
    try:
        zz.plot.font(kor=True)
        if not main(code):
            discord.message("> :zzz: 오늘은 휴장일 입니다. :zzz:")
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
        response = discord.create_thread(exc_str[:10], response.json()["id"])
        discord.message(traceback.format_exc(), "python", response.json()["id"])
