from typing import TYPE_CHECKING
import math

if TYPE_CHECKING:  # Avoid circular import issues
    from triangles import Triangles, Triangle


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance_to(self, other: "Point") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    # Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

class PointSet:
    def __init__(self, points: list[Point]) -> None:
        self.points = points
        self.point_count = len(points)

    @classmethod
    def from_bytes(cls, data: bytes) -> "PointSet":
        # Placeholder pour la méthode qui vas convertir nos bytes en PointSet
        pass

    def to_bytes(self) -> bytes:
        # Placeholder pour la méthode qui vas convertir notre PointSet en bytes
        pass

    def triangulate(self) -> "Triangles":
        from services import BowerWatsonService
        from classes.triangles import Triangles, Triangle

        super_triangle = BowerWatsonService.super_triangle(self.points)
        triangulation : list[Triangle] = [super_triangle]

        #Boucle sur tous les points du PointSet pour trouver les triangles qui ne respectent pas la condition du cercle circonscrit
        for point in self.points:
            bad_triangle : list[Triangle] = []

            # Trouver les triangles dont le cercle circonscrit contient le point
            for triangle in triangulation:
                if triangle.is_point_in_circumcircle(point):
                    bad_triangle.append(triangle)

            # Trouver les arêtes frontières des triangles "mauvais"
            polygon = []
            for triangle in bad_triangle:
                for edge in triangle.edges:
                    shared = False
                    #0n vérifie si l'arête est partagée avec un autre triangle "mauvais"
                    for other_triangle in bad_triangle:
                        if triangle == other_triangle : continue

                        #On compare les arêtes en faisant attention au sens A-B vs B-A
                        other_edges = other_triangle.edges
                        point_a, point_b = edge[0], edge[1]

                        #On vérifie si l'arête est partagée dans l'autre triangle dans les deux sens
                        for other_edge in other_edges:
                            if (other_edge[0] == point_a and other_edge[1] == point_b) or (other_edge[0] == point_b and other_edge[1] == point_a):
                                shared = True
                                break
                        if shared: break

                    #Si l'arête n'est pas partagée, c'est une arête frontière
                    if not shared:
                        polygon.append(edge)

            #Supprimer les triangles "mauvais" de la triangulation
            for triangle in bad_triangle:
                triangulation.remove(triangle)

            #Relier point a chaque arête du polygone pour former de nouveaux triangles
            for edge in polygon:
                new_triangle = Triangle(edge[0], edge[1], point)
                triangulation.append(new_triangle)

        #Retirer les triangles qui utilisent les sommets du super-triangle
        final_triangles : list[Triangle] = []
        super_points = {super_triangle.p1, super_triangle.p2, super_triangle.p3}

        for triangle in triangulation:
            if not (triangle.p1 in super_points or triangle.p2 in super_points or triangle.p3 in super_points):
                final_triangles.append(triangle)

        #Converir la liste de triangles en un  objet Triangles
        return Triangles(self,final_triangles)

    # Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        return (
            isinstance(other, PointSet)
            and self.point_count == other.point_count
            and self.points == other.points
        )
