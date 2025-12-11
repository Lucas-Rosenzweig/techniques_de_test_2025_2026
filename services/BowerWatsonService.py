from classes.pointset import Point
from classes.triangles import Triangle


def super_triangle(points : list[Point]) -> Triangle:
    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)

    # Calculs des dimension de la boîte qui englobe tous les points
    dx = max_x - min_x  # Largeur de la boîte
    dy = max_y - min_y  # Hauteur de la boîte
    delta_max = max(dx, dy)  # Plus grande dimension
    mid_x = (min_x + max_x) / 2  # Centre en x
    mid_y = (min_y + max_y) / 2  # Centre en y

    # Création du super-triangle
    p1 = Point(mid_x - 20 * delta_max, mid_y - delta_max)
    p2 = Point(mid_x, mid_y + 20 * delta_max)
    p3 = Point(mid_x + 20 * delta_max, mid_y - delta_max)
    return Triangle(p1, p2, p3)