"""Service for the Bowyer-Watson triangulation algorithm.

This module provides the implementation of the Bowyer-Watson algorithm
for Delaunay triangulation.
"""

from classes.pointset import Point
from classes.triangles import Triangle


def super_triangle(points: list[Point]) -> Triangle:
    """Create a super-triangle that encompasses all points in the list.

    Args:
        points (list[Point]): The list of points to encompass.

    Returns:
        Triangle: A triangle that contains all the points.

    """
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


def add_point_to_triangulation(point: Point, triangulation: list["Triangle"]) -> None:
    """Ajoute un point à la triangulation en utilisant l'algorithme de Bowyer-Watson."""
    from classes.triangles import Triangle

    bad_triangles = find_bad_triangles(point, triangulation)
    polygon = find_boundary_edges(bad_triangles)

    # Supprimer les triangles "mauvais"
    for triangle in bad_triangles:
        triangulation.remove(triangle)

    # Créer de nouveaux triangles avec le point
    for edge in polygon:
        new_triangle = Triangle(edge[0], edge[1], point)
        triangulation.append(new_triangle)


def find_bad_triangles(
    point: Point, triangulation: list["Triangle"]
) -> list["Triangle"]:
    """Trouve les triangles dont le cercle circonscrit contient le point."""
    bad_triangles = []
    for triangle in triangulation:
        if triangle.is_point_in_circumcircle(point):
            bad_triangles.append(triangle)
    return bad_triangles


def find_boundary_edges(bad_triangles: list["Triangle"]) -> list[tuple[Point, Point]]:
    """Trouve les arêtes frontières des triangles "mauvais"."""
    polygon = []
    for triangle in bad_triangles:
        for edge in triangle.edges:
            if not is_edge_shared(edge, triangle, bad_triangles):
                polygon.append(edge)
    return polygon


def is_edge_shared(
    edge: tuple[Point, Point],
    current_triangle: "Triangle",
    bad_triangles: list["Triangle"],
) -> bool:
    """Vérifie si une arête est partagée avec un autre triangle "mauvais"."""
    for other_triangle in bad_triangles:
        if current_triangle == other_triangle:
            continue

        for other_edge in other_triangle.edges:
            if are_edges_equal(edge, other_edge):
                return True
    return False


def are_edges_equal(edge1: tuple[Point, Point], edge2: tuple[Point, Point]) -> bool:
    """Vérifie si deux arêtes sont égales, indépendamment de l'ordre des points."""
    return (edge1[0] == edge2[0] and edge1[1] == edge2[1]) or (
        edge1[0] == edge2[1] and edge1[1] == edge2[0]
    )


def remove_super_triangle_vertices(
    triangles: list[Triangle], super_triangle: Triangle
) -> list[Triangle]:
    """Retire les triangles qui utilisent les sommets du super-triangle."""
    super_points = {super_triangle.p1, super_triangle.p2, super_triangle.p3}
    final_triangles = []

    for triangle in triangles:
        if not (
            triangle.p1 in super_points
            or triangle.p2 in super_points
            or triangle.p3 in super_points
        ):
            final_triangles.append(triangle)

    return final_triangles
