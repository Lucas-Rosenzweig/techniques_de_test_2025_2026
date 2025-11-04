#Unit test for the triangulator module
from pointset import PointSet
from pointset import Point
from triangles import Triangles

class TestTriangulate:
    def test_triangulate_must_return_valid_triangles(self):
        point_set = PointSet(3, [Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0)])
        triangulation = point_set.triangulate()
        assert isinstance(triangulation, Triangles)

    def test_triangulate_with_collinear_points(self):
        point_set = PointSet(3, [Point(1.0, 1.0), Point(2.0, 2.0), Point(3.0, 3.0)])
        expected_triangles = Triangles(point_set, 0, [])
        assert point_set.triangulate() == expected_triangles # Doit retourner une erreur

    def test_triangulate_with_void_point_set(self):
        void_point_set = PointSet(0, [])
        void_triangles = Triangles(void_point_set, 0, [])
        assert void_point_set.triangulate() == void_triangles

    def test_triangulate_with_duplicated_points(self):
        point_set = PointSet(3, [Point(1.0, 1.0),Point(1.0, 1.0), Point(2.0, 2.0)])
        expected_triangles = Triangles(point_set, 0, [])
        assert point_set.triangulate() == expected_triangles

    def test_triangulate_with_one_point(self):
        point_set = PointSet(1, [Point(1.0, 1.0)])
        expected_triangles = Triangles(point_set, 0, [])
        assert point_set.triangulate() == expected_triangles

    def test_triangulate_with_two_points(self):
        point_set = PointSet(2, [Point(1.0, 1.0), Point(2.0, 2.0)])
        expected_triangles = Triangles(point_set, 0, [])
        assert point_set.triangulate() == expected_triangles

    def test_triangulate_with_three_points(self):
        point_set = PointSet(3, [Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0)])
        triangulation = point_set.triangulate()
        assert triangulation.triangle_count == 1

    def test_triangulate_with_square_points(self):
        point_set = PointSet(4, [Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)])
        triangulation = point_set.triangulate()
        assert triangulation.triangle_count == 2

class TestTrigulatorApi:
    pass