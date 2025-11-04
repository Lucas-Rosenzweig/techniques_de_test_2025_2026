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
    def __init__(self, point_count : int, points: List[Point]) -> None:
        self.point_count = point_count
        self.points = points

    def triangulate(self) -> "Triangles":
        # Placeholder triangulation logic
        from triangles import Triangles # Local import to avoid circular dependency
        return None

    #Overriding equality operator for testing purposes
    def __eq__(self, other) -> bool:
        return (isinstance(other, PointSet) and
                self.point_count == other.point_count and
                self.points == other.points)

#Methode outside of class to create a PointSet from api data
def create_pointset_from_api_data() -> PointSet:
    # Placeholder for creating a PointSet from API data
    return None