import json
import os
import traceback

import zerohertzLib as zz
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

KEY = json.loads(os.environ.get("KEY"))
PROPERTY_ID = os.environ.get("PROPERTY_ID")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_BOT_CHANNEL = os.environ.get("DISCORD_BOT_CHANNEL")
PER = os.environ.get("PER")
ETC_PAGE = 4


def get_ga4_service(KEY):
    scope = "https://www.googleapis.com/auth/analytics.readonly"
    credentials = Credentials.from_service_account_info(KEY, scopes=[scope])
    service = build("analyticsdata", "v1beta", credentials=credentials)
    return service


def get_data(tar):
    response = (
        ga4_service.properties()
        .runReport(
            property=f"properties/{PROPERTY_ID}",
            body={
                "dimensions": [{"name": tar}],
                "metrics": [{"name": "totalUsers"}, {"name": "averageSessionDuration"}],
                "dateRanges": [{"startDate": f"{PER}daysAgo", "endDate": "yesterday"}],
            },
        )
        .execute()
    )
    return response


def make_barh(title, response, discord, thread_id):
    tmp_people = {}
    tmp_time = {}
    for row in response["rows"][::-1]:
        key = (
            row["dimensionValues"][0]["value"]
            .replace(" | Zerohertz", "")
            .replace("https://", "")[:60]
        )
        tmp_people[key] = int(row["metricValues"][0]["value"])
        tmp_time[key] = round(float(row["metricValues"][1]["value"]))
    peop = {}
    time = {}
    max_ylab = 0
    for i, (key, value) in enumerate(tmp_people.items()):
        if int(PER) > 1:
            if value > ETC_PAGE:
                peop[key] = value
                time["\n" * i] = tmp_time[key]
                max_ylab = max(max_ylab, len(key))
        else:
            peop[key] = value
            time["\n" * i] = tmp_time[key]
            max_ylab = max(max_ylab, len(key))
    zz.plot.figure((max(15, max_ylab // 3), max(10, 3 + int(len(peop) / 2.4))))
    zz.plot.subplot(1, 2, 1)
    zz.plot.barh(peop, "Number of People", title=title, rot=0, dim="명", sign=0)
    zz.plot.subplot(1, 2, 2)
    zz.plot.barh(time, "Time [sec]", title=title, rot=0, dim="초", sign=0)
    path = zz.plot.savefig(title, 100)
    discord.file(path, thread_id)


def main(tar, discord):
    if int(PER) <= 2:
        day = "day"
    else:
        day = "days"
    response = discord.message(f"> :rocket: {PER}{day} Report")
    thread_id = discord.get_thread_id(response, name=f"> :rocket: {PER}{day} Report")
    for t, tit in tar.items():
        response = get_data(t)
        make_barh(tit, response, discord, thread_id)


if __name__ == "__main__":
    ga4_service = get_ga4_service(KEY)
    discord = zz.api.DiscordBot(DISCORD_BOT_TOKEN, DISCORD_BOT_CHANNEL)
    tar = {
        "city": "City",
        "firstUserSource": "First User Source",
        "pageTitle": "Page Title",
        "pageReferrer": "Page Referrer",
    }
    try:
        zz.plot.font(kor=True)
        main(tar, discord)
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
