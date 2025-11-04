from typing import List
from Triangles import Triangles


class Point:
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y


class PointSet:
    def __init__(self, point_count : int, points: List[Point]) -> None:
        self.point_count = point_count
        self.points = points

    def triangulate(self) -> Triangles:
        # Placeholder triangulation logic
        return Triangles(self, 0, [])

#Methode outside of class to create a PointSet from api data
def create_pointset_from_api_data() -> PointSet:
    # Placeholder for creating a PointSet from API data
    return PointSet(0, [])