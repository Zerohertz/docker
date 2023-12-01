import json
import os

import zerohertzLib as zz
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from matplotlib import pyplot as plt

KEY = json.loads(os.environ.get("KEY"))
PROPERTY_ID = os.environ.get("PROPERTY_ID")
SLACK = os.environ.get("SLACK")
PER = os.environ.get("PER")


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


def make_barv(title, response):
    tmp_people = {}
    tmp_time = {}
    for row in response["rows"]:
        if "zerohertz.github.io" in row["dimensionValues"][0]["value"]:
            continue
        key = (
            row["dimensionValues"][0]["value"]
            .replace(" | Zerohertz", "")
            .replace("https://", "")[:20]
        )
        tmp_people[key] = int(row["metricValues"][0]["value"])
        tmp_time[key] = round(float(row["metricValues"][1]["value"]))
    peop = {}
    time = {}
    etc_p = etc_t = 0
    for key, value in tmp_people.items():
        if PER == 1:
            peop[key] = value
            time[key] = tmp_time[key]
        else:
            if value >= 5:
                peop[key] = value
                time[key] = tmp_time[key]
            else:
                etc_p += value
                etc_t += tmp_time[key]
    if int(PER) > 1:
        peop["Etc"], time["Etc"] = etc_p, etc_t
    zz.plot.figure((30, 10))
    plt.subplot(1, 2, 1)
    zz.plot.barv(peop, title, "Number of People", "People", rot=45, save=False)
    plt.subplot(1, 2, 2)
    zz.plot.barv(time, title, "Time [sec]", "Time", rot=45, save=False)
    zz.plot.savefig(title, 100)


def main(tar, slack):
    for t, tit in tar.items():
        response = get_data(t)
        make_barv(tit, response)
        slack.message(f"> :rocket: {tit}")
        slack.file(f"{tit.lower().replace(' ', '_')}.png")


if __name__ == "__main__":
    ga4_service = get_ga4_service(KEY)
    slack = zz.api.SlackBot(
        SLACK, "zerohertz", name="Google Analytics 4", icon_emoji="bar_chart"
    )
    tar = {
        "city": "City",
        "firstUserSource": "First User Source",
        "pageTitle": "Page Title",
        "pageReferrer": "Page Referrer",
    }
    main(tar, slack)
