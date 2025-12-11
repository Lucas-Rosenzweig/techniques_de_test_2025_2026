from classes.pointset import Point, PointSet


class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    # Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Triangle)
            and self.p1 == other.p1
            and self.p2 == other.p2
            and self.p3 == other.p3
        )

class TriangleIndex:
    def __init__(self, i1: int, i2: int, i3: int) -> None:
        self.i1 = i1
        self.i2 = i2
        self.i3 = i3

    # Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        return (
            isinstance(other, TriangleIndex)
            and self.i1 == other.i1
            and self.i2 == other.i2
            and self.i3 == other.i3
        )

class Triangles:
    """
    Représente un ensemble de triangles dont les sommets sont des points d'un PointSet.

    En interne, stocke des objets Triangle (avec des Points) pour faciliter l'algorithme
    de triangulation (notamment pour le super-triangle qui contient des points hors du PointSet).

    Représentation binaire:
    - Partie 1: PointSet (sommets)
      * 4 bytes: nombre de points (unsigned long)
      * Pour chaque point: 8 bytes (4 bytes float X + 4 bytes float Y)
    - Partie 2: Triangles
      * 4 bytes: nombre de triangles (unsigned long)
      * Pour chaque triangle: 12 bytes (3 x 4 bytes unsigned long = indices des 3 sommets)
    """
    def __init__(self, pointset: PointSet, triangles: list[Triangle]) -> None:
        self.pointset = pointset
        self.triangles = triangles
        self.triangle_count = len(triangles)

    # Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Triangles)
            and self.pointset == other.pointset
            and self.triangle_count == other.triangle_count
            and self.triangles == other.triangles
        )

    def add(self,triangle : Triangle) -> None:
        self.triangles.append(triangle)
        self.triangle_count += 1

    def to_bytes(self) -> bytes:
        # Placeholder pour la méthode qui vas convertir notre Triangles en bytes
        # Lors de la sérialisation, on convertira les Triangle (Points) en indices
        # en cherchant chaque point dans self.pointset.points
        pass
