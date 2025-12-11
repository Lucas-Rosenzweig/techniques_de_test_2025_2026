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
            BowerWatsonService.add_point_to_triangulation(point, triangulation)

        final_triangles = BowerWatsonService.remove_super_triangle_vertices(triangulation,super_triangle)
        return Triangles(self, final_triangles)

    # Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        return (
            isinstance(other, PointSet)
            and self.point_count == other.point_count
            and self.points == other.points
        )
