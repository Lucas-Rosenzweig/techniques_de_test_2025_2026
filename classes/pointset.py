from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Avoid circular import issues
    from triangles import Triangles


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    # Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        return isinstance(other, Point) and self.x == other.x and self.y == other.y


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
        from classes.triangles import Triangles

        super_triangles = BowerWatsonService.super_triangle(self.points)
        triangulation = Triangles(self, []) # Initialisation vide des triangles
        triangulation.add(super_triangles) # Ajout du super-triangle dans la triangulation
        return triangulation

    # Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        return (
            isinstance(other, PointSet)
            and self.point_count == other.point_count
            and self.points == other.points
        )
