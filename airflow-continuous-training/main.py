import os

import matplotlib.pyplot as plt
import numpy as np
import psycopg2
import requests
from sklearn.tree import DecisionTreeClassifier

WEBHOOK = os.environ.get("WEBHOOK")
CLASSES = eval(os.environ.get("CLASSES"))
TIME = os.environ.get("TIME")
QUERY = os.environ.get("QUERY")
user = os.environ.get("user")
password = os.environ.get("password")
host = os.environ.get("host")
port = os.environ.get("port")
database = os.environ.get("database")


def execute_query(query):
    with psycopg2.connect(
        user=user, password=password, host=host, port=port, database=database
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
    return records


def main():
    data = execute_query(QUERY)
    X = np.array([[item[1], item[2]] for item in data])
    y = np.array([CLASSES.index(item[3]) for item in data])

    clf = DecisionTreeClassifier()
    clf.fit(X, y)

    plt.figure(figsize=(10, 10))
    ax = plt.gca()

    xlim = (-7, 7)
    ylim = (-7, 7)

    xx = np.linspace(xlim[0], xlim[1], 500)
    yy = np.linspace(ylim[0], ylim[1], 500)

    YY, XX = np.meshgrid(yy, xx)
    xy = np.vstack([XX.ravel(), YY.ravel()]).T
    Z = clf.predict(xy)

    n_classes = len(CLASSES)
    colors = plt.cm.jet(np.linspace(0, 1, n_classes))

    ax.contourf(
        XX, YY, Z.reshape(XX.shape), levels=n_classes - 1, colors=colors, alpha=0.5
    )
    scatter = ax.scatter(
        X[:, 0], X[:, 1], c=y, marker="o", edgecolors="k", cmap=plt.cm.jet
    )

    legend_handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=f"CLASS {CLASSES[i]}",
            markersize=10,
            markerfacecolor=colors[i],
        )
        for i in range(n_classes)
    ]
    ax.legend(handles=legend_handles, loc="upper right")

    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.title(TIME)
    plt.grid()
    plt.savefig("result.png", bbox_inches="tight")

    with open("result.png", "rb") as f:
        files = {"file": (f"{TIME}.png", f, "image/png")}
        requests.post(WEBHOOK, files=files)


if __name__ == "__main__":
    main()
