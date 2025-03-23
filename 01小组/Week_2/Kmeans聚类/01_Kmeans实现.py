import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt


def calculate_distance(x, y):
    distance = np.linalg.norm(x - y)
    return distance


class KMeans:
    def __init__(self, n_clusters=3, max_iter=100):
        self.data = None
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.X = None
        self.Y = None

    def read_data(self, filename="./iris_data/iris.csv"):
        self.data = pd.read_csv(filename)
        self.X, self.Y = self.data.iloc[:, 1: -1], self.data.iloc[:, -1]
        self.X = self.X.values

    def get_clusters(self, clusters_center):
        distances = np.linalg.norm(self.X[:, np.newaxis] - clusters_center, axis=2)
        new_clusters = np.argmin(distances, axis=1)
        return new_clusters

    def update_clusters(self, new_clusters):
        new_center = []
        for i in range(self.n_clusters):
            sum = np.zeros(self.X.shape[1])
            cnt = 0
            for j in range(self.X.shape[0]):
                if new_clusters[j] == i:
                    cnt += 1
                    sum += self.X[j]
            mean = sum / cnt
            new_center.append(mean)
        new_center = np.array(new_center)
        return new_center

    def classify(self):
        clusters_center = np.array(random.sample(self.X.tolist(), self.n_clusters))
        for _ in range(self.max_iter):
            new_clusters = self.get_clusters(clusters_center)
            clusters_center = self.update_clusters(new_clusters)
            print(clusters_center)

        return clusters_center

    def evaluate(self):
        clusters_center = self.classify()
        classify_distance = self.get_clusters(clusters_center)

        iris_dataset = self.data.iloc[:, 1:].to_numpy()
        print(clusters_center)


if __name__ == '__main__':
    kmeans = KMeans()
    kmeans.read_data()
    kmeans.classify()
    kmeans.evaluate()
