# Unit test for the triangulator module
import struct
import pytest

from classes.pointset import Point, PointSet
from classes.triangles import Triangles


class TestTriangulate:
    def test_triangulate_must_return_triangles(self):
        point_set = PointSet([Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0)])
        triangulation = point_set.triangulate()
        assert isinstance(triangulation, Triangles)

    def test_triangulate_must_return_valid_triangle(self):
        point_set = PointSet([Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0)])
        triangulation = point_set.triangulate()
        assert triangulation.triangle_count == 1

    def test_triangulate_with_collinear_points(self):
        collinear_point_set = PointSet(
            [Point(1.0, 1.0), Point(2.0, 2.0), Point(3.0, 3.0)]
        )
        with pytest.raises(
            ValueError, match="Cannot triangulate a PointSet with only collinear points"
        ):
            collinear_point_set.triangulate()

    def test_triangulate_with_void_point_set(self):
        void_point_set = PointSet([])
        with pytest.raises(ValueError, match="Cannot triangulate an empty PointSet"):
            void_point_set.triangulate()

    def test_triangulate_with_duplicated_points(self):
        duplicated_point_point_set = PointSet(
            [Point(1.0, 1.0), Point(1.0, 1.0), Point(2.0, 2.0)]
        )
        with pytest.raises(
            ValueError, match="Cannot triangulate a PointSet with duplicated points"
        ):
            duplicated_point_point_set.triangulate()

    def test_triangulate_with_one_point(self):
        point_set = PointSet([Point(1.0, 1.0)])
        with pytest.raises(
            ValueError, match="Cannot triangulate a PointSet with less than 3 points"
        ):
            point_set.triangulate()

    def test_triangulate_with_two_points(self):
        point_set = PointSet([Point(1.0, 1.0), Point(2.0, 2.0)])
        with pytest.raises(
            ValueError, match="Cannot triangulate a PointSet with less than 3 points"
        ):
            point_set.triangulate()

    def test_triangulate_with_three_points(self):
        point_set = PointSet([Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0)])
        triangulation = point_set.triangulate()
        assert triangulation.triangle_count == 1

    def test_triangulate_with_square_points(self):
        point_set = PointSet(
            [Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)]
        )
        triangulation = point_set.triangulate()
        assert triangulation.triangle_count == 2


class TestSerialization:
    def test_pointset_to_bytes_must_return_bytes(self):
        point_set = PointSet([Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0)])
        point_set_bytes = point_set.to_bytes()
        valid_point_set_bytes = struct.pack(
            '<Lffffff',  # L = unsigned long, f = float (little-endian)
            3,           # nombre de points
            0.0, 0.0,    # point 1 (x, y)
            1.0, 0.0,    # point 2 (x, y)
            1.0, 1.0     # point 3 (x, y)
        )
        assert point_set_bytes == valid_point_set_bytes
        assert isinstance(point_set_bytes, bytes)

    def test_triangles_to_bytes_must_return_bytes(self):
        point_set = PointSet([Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0)])
        triangles = point_set.triangulate()
        triangles_bytes = triangles.to_bytes()
        valid_triangles_bytes = struct.pack(
            '<LffffffLLLL',
            3,        # nombre de points (unsigned long)
            0.0, 0.0, # point 1
            1.0, 0.0, # point 2
            1.0, 1.0, # point 3
            1,        # nombre de triangles (unsigned long)
            0, 1, 2   # indices des 3 sommets du triangle (unsigned long chacun)
        )
        assert triangles_bytes == valid_triangles_bytes
        assert isinstance(triangles_bytes, bytes)


class TestDeserialization:
    def test_pointset_from_bytes_must_return_pointset(self):
        # Sérialisation manuelle: 2 points (5.0, 7.0) et (3.0, 4.0)
        # 4 bytes: nombre de points (2)
        # 8 bytes: point 1 (5.0, 7.0)
        # 8 bytes: point 2 (3.0, 4.0)
        point_set_bytes = struct.pack(
            '<Lffff',
            2,        # nombre de points (unsigned long)
            5.0, 7.0, # point 1
            3.0, 4.0  # point 2
        )
        point_set = PointSet.from_bytes(point_set_bytes)
        valid_point_set = PointSet([Point(5.0, 7.0), Point(3.0, 4.0)])
        assert point_set == valid_point_set
        assert isinstance(point_set, PointSet)