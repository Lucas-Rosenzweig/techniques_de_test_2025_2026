#Unit test for the triangulator module
from pointset import PointSet
from triangles import Triangles


def test_triangulate_with_void_point_set():
    void_point_set = PointSet(0, [])
    void_triangles = Triangles(void_point_set, 0, [])
    assert void_point_set.triangulate() == void_triangles
