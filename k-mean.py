import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_centroid(points: list):
    """Расчитывает центроид для одного кластера. Возвращает центроид"""
    # points = [(1,3), (1,2), (1,1)]
    sums = []
    for i in range(len(points[0])):
        s = 0
        for point in points:
            s += point[i]
        sums.append(s)
    return tuple(i / len(points) for i in sums)


def error_square(clusters: dict):
    """Расчитывает ошибку для одного класетра. Возвращает значение ошибки"""
    error = 0
    for c, points in clusters.items():
        for p in points:
            for coordinate in range(len(c)):
                error += (c[coordinate] - p[coordinate]) ** 2
    return error


def create_distance(centroid, points):
    """Расчитывает растояние между центроидом и набором точек"""
    distance = dict.fromkeys(points, None)
    for point in points:
        s = 0
        for coordinate in range(len(point)):
            s += (centroid[coordinate] - point[coordinate]) ** 2
        distance[point] = s ** 0.5
    return distance


def create_distance_from_point(centroids, point):
    """Находит все расстояния точки от всех центродов"""
    distance = {}
    for c in centroids:
        s = 0
        for coordinate in range(len(point)):
            s += (c[coordinate] - point[coordinate]) ** 2
        distance[c] = s ** 0.5
    return distance


def main_loop():
    # clusters =
    #     {
    #     (1, 1): [(1, 3), (1, 2), (1, 1)],
    #     (2, 1): [(3, 3), (4, 3), (5, 3), (2, 1), (4, 2)]
    #     }
    df = pd.read_csv("passwd.csv")
    df = df[['mathematics', 'physics', 'chemistry', 'english']] #"Open", "High", "Low",
    points = np.array(df)
    centroid = points[np.random.choice(np.arange(points.shape[0]), size=5, replace=False)]
    points = [tuple(x) for x in points]
    centroid = [tuple(x) for x in centroid]
    #points = [(1, 3, 3), (1, 2, 3), (1, 1, 3), (3, 3, 3), (4, 3, 3), (5, 3, 3), (2, 1, 3), (4, 2, 3)]
    # centroid = [(1, 1, 3), (2, 1, 3)]
    cluster = fill_clusters(centroid, points)
    old_cluster = None
    while old_cluster != cluster:
        old_cluster = cluster
        print(error_square(cluster))
        centroid = [create_centroid(p) for p in cluster.values()]
        cluster = fill_clusters(centroid, points)
    print(cluster)
    print(cluster.keys())
    # x = np.array([1, 2, 3, 4])
    # y = df[df == 5].count().values
    fig, ax = plt.subplots(figsize=[16, 16])
    # ax[0].stem(x, y)
    # ax[0].set_xticks(x, labels=['mathematics', 'physics', 'chemistry', 'english'])
    # ax[0].set_yticks(y, y)
    x = [round(np.mean(cl), 2) for cl in cluster.keys()]
    y = []
    for centroid, points in cluster.items():
        y.append(len(points))
    ax.stem(x, y)
    ax.set(xticks=list(ax.get_xticks()[0]) + [int(i) for i in x], xlim=(0, 5))
    # ax.set_xticks(x, x)
    ax.set_yticks(y, y)
    plt.show()
    print(df[df == 5].count().values)
    print(df[df == 5].count())


def fill_clusters(centroid, points):
    cluster = {}
    for i in centroid:
        cluster[i] = []
    for p in points:
        distance = create_distance_from_point(centroid, p)
        # print(f"Point: {p}  distance: {distance}")
        m = min(distance.values())
        for key, value in distance.items():
            if value == m:
                cluster[key].append(p)
    return cluster


if __name__ == '__main__':
    main_loop()
