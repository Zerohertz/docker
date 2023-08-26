import json
import os

import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

KEY = json.loads(os.environ.get("KEY"))
PROPERTY_ID = os.environ.get("PROPERTY_ID")
WEBHOOK = os.environ.get("WEBHOOK")


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
                "metrics": [{"name": "totalUsers"}],
                "dateRanges": [{"startDate": "1daysAgo", "endDate": "yesterday"}],
            },
        )
        .execute()
    )
    return response


def get_message(title, response):
    message = f"# :rocket: {title}\n```"
    for row in response["rows"]:
        # if int(row["metricValues"][0]["value"]) > 2:
        message += (
            row["dimensionValues"][0]["value"].replace("https://", "")
            + ":\t"
            + row["metricValues"][0]["value"]
            + "\n"
        )
    message += "```"
    return message


def send_discord_message(webhook_url, content):
    data = {"content": content}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    return response


def main(tar):
    for t, tit in tar.items():
        response = get_data(t)
        message = get_message(tit, response)
        send_discord_message(WEBHOOK, message)


if __name__ == "__main__":
    ga4_service = get_ga4_service(KEY)
    tar = {
        "city": "City",
        "firstUserSource": "First User Source",
        # "pageReferrer": "Page Referrer",
    }
    main(tar)
