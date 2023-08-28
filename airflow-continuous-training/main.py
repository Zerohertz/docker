import datetime
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import requests
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

WEBHOOK = os.environ.get("WEBHOOK")
CLASSES = eval(os.environ.get("CLASSES"))
TIME = os.environ.get("TIME")

def main():
    data = sys.argv[1]
    data = eval(data.replace(", tzinfo=Timezone('UTC')", ""))
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

    contour = ax.contourf(XX, YY, Z.reshape(XX.shape), levels=n_classes-1, colors=colors, alpha=0.5)
    plt.colorbar(contour)

    scatter = ax.scatter(X[:, 0], X[:, 1], c=y, marker="o", edgecolors="k", cmap=plt.cm.jet)
    
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.title(TIME)
    plt.savefig("result.png", bbox_inches="tight")

    with open("result.png", "rb") as f:
        files = {"file": (f"{TIME}.png", f, "image/png")}
        requests.post(WEBHOOK, files=files)


if __name__ == "__main__":
    main()
