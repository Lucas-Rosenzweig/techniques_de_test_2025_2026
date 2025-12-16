"""PointSet and Point classes.

This module defines the Point and PointSet classes used for triangulation.
"""

import math
import struct
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Avoid circular import issues
    from triangles import Triangles


class Point:
    """Represents a point in 2D space."""

    def __init__(self, x: float, y: float) -> None:
        """Initialize a Point.

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.

        """
        self.x = x
        self.y = y

    def distance_to(self, other: "Point") -> float:
        """Calculate the Euclidean distance to another point.

        Args:
            other (Point): The other point.

        Returns:
            float: The distance between the two points.

        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    # Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        """Check equality with another object."""
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """Return the hash of the point."""
        return hash((self.x, self.y))


class PointSet:
    """Represents a set of points."""

    def __init__(self, points: list[Point]) -> None:
        """Initialize a PointSet.

        Args:
            points (list[Point]): The list of points.

        """
        self.points = points
        self.point_count = len(points)

    @classmethod
    def from_bytes(cls, data: bytes) -> "PointSet":
        """Deserialize a PointSet from bytes.

        Args:
            data (bytes): The byte representation of the PointSet.

        Returns:
            PointSet: The deserialized PointSet.

        """
        offset = 0
        (point_count,) = struct.unpack_from("<L", data, offset)
        offset += 4
        points = []
        for _ in range(point_count):
            x, y = struct.unpack_from("<ff", data, offset)
            points.append(Point(x, y))
            offset += 8
        return cls(points)

    def to_bytes(self) -> bytes:
        """Serialize the PointSet to bytes.

        Returns:
            bytes: The byte representation of the PointSet.

        """
        data = bytearray()
        data.extend(struct.pack("<L", self.point_count))
        for point in self.points:
            data.extend(struct.pack("<ff", point.x, point.y))
        return bytes(data)

    # Fonction qui vérifie si tous les points sont colinéaires
    def check_colinearity(self) -> bool:
        """Check if all points in the set are collinear.

        Returns:
            bool: True if all points are collinear, False otherwise.

        """
        p1 = self.points[0]
        p2 = self.points[1]

        for i in range(2, self.point_count):
            p = self.points[i]
            # Calcul du déterminant pour vérifier la colinéarité
            if (p2.x - p1.x) * (p.y - p1.y) != (p.x - p1.x) * (p2.y - p1.y):
                return False  # Trouvé un point non colinéaire

        return True  # Tous les points sont colinéaires

    def check_duplicates(self) -> bool:
        """Check for duplicate points in the set.

        Returns:
            bool: True if duplicates exist, False otherwise.

        """
        seen = set()
        for point in self.points:
            if point in seen:
                return True
            seen.add(point)
        return False

    def triangulate(self) -> "Triangles":
        """Triangulate the PointSet using the Bowyer-Watson algorithm.

        Returns:
            Triangles: The resulting triangulation.

        Raises:
            ValueError: If the PointSet is invalid
                (empty, <3 points, collinear, duplicates).

        """
        from classes.triangles import Triangle, Triangles
        from services import BowerWatsonService

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
        triangulation: list[Triangle] = [super_triangle]

        # Boucle sur tous les points du PointSet pour trouver les triangles
        # qui ne respectent pas la condition du cercle circonscrit
        for point in self.points:
            BowerWatsonService.add_point_to_triangulation(point, triangulation)

        final_triangles = BowerWatsonService.remove_super_triangle_vertices(
            triangulation, super_triangle
        )
        return Triangles(self, final_triangles)

    # Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        """Check equality with another object."""
        return (
            isinstance(other, PointSet)
            and self.point_count == other.point_count
            and self.points == other.points
        )
