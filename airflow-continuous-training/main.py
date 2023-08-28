import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import requests
from sklearn import svm

WEBHOOK = os.environ.get("WEBHOOK")


def main():
    data = sys.argv[1]
    X = np.array([[item[1], item[2]] for item in data])
    y = np.array([item[3] for item in data])
    clf = svm.SVC(kernel="linear")
    clf.fit(X, y)
    plt.scatter(X[:, 0], X[:, 1], c=y, marker="o", edgecolors="k")
    ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    xx = np.linspace(xlim[0], xlim[1])
    yy = np.linspace(ylim[0], ylim[1])
    YY, XX = np.meshgrid(yy, xx)
    xy = np.vstack([XX.ravel(), YY.ravel()]).T
    Z = clf.decision_function(xy).reshape(XX.shape)
    ax.contour(
        XX,
        YY,
        Z,
        colors="k",
        levels=[-1, 0, 1],
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
    plt.savefig("result.png", bbox_inches="tight")
    with open("result.png", "rb") as f:
        files = {"file": ("result.png", f, "image/png")}
        requests.post(WEBHOOK, files=files)


if __name__ == "__main__":
    main()
