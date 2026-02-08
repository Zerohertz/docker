import os
import traceback
from datetime import datetime

import zerohertzLib as zz

SYMBOLS = os.environ.get("SYMBOLS")
if "," in SYMBOLS:
    SYMBOLS = SYMBOLS.split(",")
else:
    SYMBOLS = int(SYMBOLS)
START_DAY = os.environ.get("START_DAY", "20220101")
TOP = int(os.environ.get("TOP", 2))
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_BOT_CHANNEL = os.environ.get("DISCORD_BOT_CHANNEL")
MP_NUM = int(os.environ.get("MP_NUM", 0))
KOR = bool(int(os.environ.get("KOR", 1)))
MODE = os.environ.get("MODE", "All")


def main(test_code):
    now = datetime.now()
    qbf = zz.quant.QuantBotFDR(
        SYMBOLS,
        start_day=START_DAY,
        ohlc="Close",
        top=TOP,
        token=DISCORD_BOT_TOKEN,
        channel=DISCORD_BOT_CHANNEL,
        mp_num=MP_NUM,
        analysis=True,
        kor=KOR,
    )
    _, test_data = qbf._get_data(test_code)
    if KOR and test_data.index[-1].day != now.day:
        return False
    if MODE == "All":
        qbf.index()
    elif MODE == "Buy":
        qbf.buy()
    return True


if __name__ == "__main__":
    if KOR:
        code = "005930"
    else:
        code = "AAPL"
    discord = zz.api.DiscordBot(DISCORD_BOT_TOKEN, DISCORD_BOT_CHANNEL)
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
        thread_id = discord.get_thread_id(response, name=exc_str)
        discord.message(traceback.format_exc(), "python", thread_id)
