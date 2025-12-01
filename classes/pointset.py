from typing import List, TYPE_CHECKING

if TYPE_CHECKING: # Avoid circular import issues
    from triangles import Triangles


class Point:
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y

    #Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        return isinstance(other, Point) and self.x == other.x and self.y == other.y


class PointSet:
    def __init__(self, points: List[Point]) -> None:
        self.points = points
        self.point_count = len(points)

    @classmethod
    def from_bytes(cls, data: bytes) -> "PointSet":
        #Placeholder pour la méthode qui vas convertir nos bytes en PointSet
        pass

    def to_bytes(self) -> bytes:
        #Placeholder pour la méthode qui vas convertir notre PointSet en bytes
        pass

    def triangulate(self) -> "Triangles":
        #Placeholder pour la méthode qui vas trianguler notre PointSet
        pass

    #Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        return (isinstance(other, PointSet) and
                self.point_count == other.point_count and
                self.points == other.points)
