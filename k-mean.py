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

    points = [(1, 3), (1, 2), (1, 1), (3, 3), (4, 3), (5, 3), (2, 1), (4, 2)]
    centroid = [(1, 1), (2, 1)]
    cluster = fill_clusters(centroid, points)
    print(cluster)
    while error_square(cluster) >= 7:
        print("=" * 50)
        centroid = [create_centroid(p) for p in cluster.values()]
        print(centroid)
        cluster = fill_clusters(centroid, points)
        print(cluster)


def fill_clusters(centroid, points):
    cluster = {}
    for i in centroid:
        cluster[i] = []
    for p in points:
        distance = create_distance_from_point(centroid, p)
        print(f"Point: {p}  distance: {distance}")
        m = min(distance.values())
        for key, value in distance.items():
            if value == m:
                cluster[key].append(p)
    return cluster


main_loop()
