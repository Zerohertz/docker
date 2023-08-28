import datetime
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import requests
from sklearn import svm

WEBHOOK = os.environ.get("WEBHOOK")
CLASSES = eval(os.environ.get("CLASSES"))
TIME = os.environ.get("TIME")


def main():
    data = sys.argv[1]
    data = eval(data.replace(", tzinfo=Timezone('UTC')", ""))
    X = np.array([[item[1], item[2]] for item in data])
    y = np.array([CLASSES.index(item[3]) for item in data])
    clf = svm.SVC(kernel="rbf", decision_function_shape="ovr")
    clf.fit(X, y)

    plt.figure(figsize=(10, 10))
    plt.scatter(X[:, 0], X[:, 1], c=y, marker="o", edgecolors="k", cmap=plt.cm.jet)
    ax = plt.gca()

    xlim = (-5, 5)
    ylim = (-5, 5)

    xx = np.linspace(xlim[0], xlim[1], 500)
    yy = np.linspace(ylim[0], ylim[1], 500)

    YY, XX = np.meshgrid(yy, xx)
    xy = np.vstack([XX.ravel(), YY.ravel()]).T
    Z = clf.decision_function(xy).reshape(XX.shape)

    ax.contour(
        XX,
        YY,
        Z,
        colors="k",
        levels=np.arange(len(CLASSES) - 1) + 0.5,
        alpha=0.5,
        linestyles=["--", "-", "--"],
    )

    ax.scatter(
        clf.support_vectors_[:, 0],
        clf.support_vectors_[:, 1],
        s=100,
        facecolors="none",
        edgecolors="k",
    )

    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.title(TIME)
    plt.savefig("result.png", bbox_inches="tight")

    with open("result.png", "rb") as f:
        files = {"file": ("result.png", f, "image/png")}
        requests.post(WEBHOOK, files=files)


if __name__ == "__main__":
    main()
