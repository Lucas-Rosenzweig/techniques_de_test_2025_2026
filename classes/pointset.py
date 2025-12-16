from typing import TYPE_CHECKING
import math
import struct

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
        offset = 0
        (point_count,) = struct.unpack_from('<L', data, offset)
        offset += 4
        points = []
        for _ in range(point_count):
            x, y = struct.unpack_from('<ff', data, offset)
            points.append(Point(x, y))
            offset += 8
        return cls(points)

    def to_bytes(self) -> bytes:
        data = bytearray()
        data.extend(struct.pack('<L', self.point_count))
        for point in self.points:
            data.extend(struct.pack('<ff', point.x, point.y))
        return bytes(data)

    #Fonction qui vérifie si tous les points sont colinéaires
    def check_colinearity(self) -> bool:
        if self.point_count < 3:
            return False  # Moins de 3 points ne peuvent pas être colinéaires

        p1 = self.points[0]
        p2 = self.points[1]

        for i in range(2, self.point_count):
            p = self.points[i]
            # Calcul du déterminant pour vérifier la colinéarité
            if (p2.x - p1.x) * (p.y - p1.y) != (p.x - p1.x) * (p2.y - p1.y):
                return False  # Trouvé un point non colinéaire

        return True  # Tous les points sont colinéaires

    def check_duplicates(self) -> bool:
        seen = set()
        for point in self.points:
            if point in seen:
                return True
            seen.add(point)
        return False

    def triangulate(self) -> "Triangles":
        from services import BowerWatsonService
        from classes.triangles import Triangles, Triangle

        # On vérifie que le PointSet est valide pour la triangulation
        if self == PointSet([]):
            raise ValueError("Cannot triangulate an empty PointSet")

        if self.point_count < 3:
            raise ValueError("Cannot triangulate a PointSet with less than 3 points")

        if self.check_colinearity():
            raise ValueError("Cannot triangulate a PointSet with only collinear points")

        if self.check_duplicates():
            raise ValueError("Cannot triangulate a PointSet with duplicated points")

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
