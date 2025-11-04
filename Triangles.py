from typing import List
from PointSet import Point
from PointSet import PointSet

class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

class Triangles:
    def __init__(self, pointset: PointSet, triangle_count:int, triangles: List[Triangle]) -> None:
        self.pointset = pointset
        self.trianglesNumber = triangle_count
        self.triangles = triangles

    def push_to_api(self) -> None:
        # Placeholder for pushing triangles to an API
        pass