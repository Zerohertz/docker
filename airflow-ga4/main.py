import json
import os
import traceback

import zerohertzLib as zz
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from matplotlib import pyplot as plt

KEY = json.loads(os.environ.get("KEY"))
PROPERTY_ID = os.environ.get("PROPERTY_ID")
SLACK = os.environ.get("SLACK")
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


def make_barh(title, response, slack, thread_ts):
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
    plt.subplot(1, 2, 1)
    zz.plot.barh(peop, "Number of People", title=title, rot=0, per=False, save=False)
    plt.subplot(1, 2, 2)
    zz.plot.barh(time, "Time [sec]", title=title, rot=0, per=False, save=False)
    path = zz.plot.savefig(title, 100)
    slack.file(path, thread_ts=thread_ts)


def main(tar, slack):
    if int(PER) <= 2:
        day = "day"
    else:
        day = "days"
    thread_ts = slack.message(f"> :rocket: {PER}{day} Report").json()["ts"]
    for t, tit in tar.items():
        response = get_data(t)
        make_barh(tit, response, slack, thread_ts)


if __name__ == "__main__":
    ga4_service = get_ga4_service(KEY)
    slack = zz.api.SlackBot(
        SLACK,
        "google_analytics_4",
        name="Google Analytics 4",
        icon_emoji="bar_chart",
        timeout=30,
    )
    tar = {
        "city": "City",
        "firstUserSource": "First User Source",
        "pageTitle": "Page Title",
        "pageReferrer": "Page Referrer",
    }
    try:
        zz.plot.font(kor=True)
        main(tar, slack)
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
