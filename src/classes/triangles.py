"""Triangle and Triangles classes.

This module defines the Triangle and Triangles classes used for triangulation.
"""

import struct

from classes.pointset import Point, PointSet


class Triangle:
    """Represents a triangle defined by 3 points."""

    def __init__(self, p1: Point, p2: Point, p3: Point) -> None:
        """Initialize a Triangle.

        Args:
            p1 (Point): The first vertex.
            p2 (Point): The second vertex.
            p3 (Point): The third vertex.

        """
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        # Calcul du cercle circonscrit pour la triangulation de Bowyer-Watson
        self.edges = [(p1, p2), (p2, p3), (p3, p1)]
        self.circumcenter = None
        self.circumradius = 0
        self.calculate_circumcircle()

    def calculate_circumcircle(self) -> None:
        """Calculate the circumcircle center and radius."""
        ax, ay = self.p1.x, self.p1.y
        bx, by = self.p2.x, self.p2.y
        cx, cy = self.p3.x, self.p3.y
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))

        # Calcul des coordonnées du centre du cercle circonscrit
        # avec la formule du déterminant
        ux = (
            (ax**2 + ay**2) * (by - cy)
            + (bx**2 + by**2) * (cy - ay)
            + (cx**2 + cy**2) * (ay - by)
        ) / d
        uy = (
            (ax**2 + ay**2) * (cx - bx)
            + (bx**2 + by**2) * (ax - cx)
            + (cx**2 + cy**2) * (bx - ax)
        ) / d

        self.circumcenter = Point(ux, uy)
        self.circumradius = self.circumcenter.distance_to(self.p1)

    def is_point_in_circumcircle(self, point: Point) -> bool:
        """Check if a point is inside the circumcircle.

        Args:
            point (Point): The point to check.

        Returns:
            bool: True if the point is inside, False otherwise.

        """
        if self.circumradius == float("inf"):
            return False  # Pas de cercle circonscrit défini pour les points colinéaires
        distance = self.circumcenter.distance_to(
            point
        )  # Distance entre le Point a vérifier et le centre du cercle circonscrit
        return (
            distance < self.circumradius
        )  # Si la distance est > rayon, le point est en dehors du cercle circonscrit

    # Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        """Check equality with another object."""
        return (
            isinstance(other, Triangle)
            and self.p1 == other.p1
            and self.p2 == other.p2
            and self.p3 == other.p3
        )


class Triangles:
    """Represents a set of triangles forming a triangulation.

    Binary Representation:
    - Part 1: PointSet (vertices)
      * 4 bytes: number of points (unsigned long)
      * For each point: 8 bytes (4 bytes float X + 4 bytes float Y)
    - Part 2: Triangles
      * 4 bytes: number of triangles (unsigned long)
      * For each triangle: 12 bytes
        (3 x 4 bytes unsigned long = indices of the 3 vertices)
    """

    def __init__(self, pointset: PointSet, triangles: list[Triangle]) -> None:
        """Initialize Triangles.

        Args:
            pointset (PointSet): The set of vertices.
            triangles (list[Triangle]): The list of triangles.

        """
        self.pointset = pointset
        self.triangles = triangles
        self.triangle_count = len(triangles)

    def to_bytes(self) -> bytes:
        """Serialize Triangles to bytes.

        Returns:
            bytes: The byte representation of the triangulation.

        """
        data = bytearray(self.pointset.to_bytes())
        data.extend(struct.pack("<L", self.triangle_count))
        for triangle in self.triangles:
            idx1 = self.pointset.points.index(triangle.p1)
            idx2 = self.pointset.points.index(triangle.p2)
            idx3 = self.pointset.points.index(triangle.p3)
            indices = sorted([idx1, idx2, idx3])
            data.extend(struct.pack("<LLL", *indices))
        return bytes(data)
