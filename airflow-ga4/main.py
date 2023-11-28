import json
import os

import zerohertzLib as zz
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from prettytable import PrettyTable

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


def get_message(title, response):
    messages = [f"> :rocket: {title}\n"]
    table = PrettyTable()
    table.field_names = [title, "People No.", "Time [sec]"]
    for row in response["rows"]:
        print(row)
        if "zerohertz.github.io" in row["dimensionValues"][0]["value"]:
            continue
        if len(str(table)) > 1500:
            messages.append("```\n" + str(table) + "\n```")
            table = PrettyTable()
            table.field_names = [title, "People No.", "Time [sec]"]
        table.add_row(
            [
                row["dimensionValues"][0]["value"]
                .replace(" | Zerohertz", "")
                .replace("https://", "")[:50],
                row["metricValues"][0]["value"],
                str(round(float(row["metricValues"][1]["value"]))),
            ]
        )
    else:
        messages.append("```\n" + str(table) + "\n```")
    return messages


def main(tar, slack):
    for t, tit in tar.items():
        response = get_data(t)
        messages = get_message(tit, response)
        for message in messages:
            slack.message(message)


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
