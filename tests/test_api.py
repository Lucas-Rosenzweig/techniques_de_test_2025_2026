#Unit test for the triangulator api
import pytest
from classes.pointset import PointSet
from classes.pointset import Point
from classes.triangles import Triangles
from Triangulator import app as flask_app

class TestTriangulatorApi:
    #Fixture for flask client
    @pytest.fixture
    def client(self):
        flask_app.config['TESTING'] = True
        with flask_app.test_client() as client:
            yield client

    def test_triangulation_endpoint(self, client):
        response = client.get("/triangulation/testPointSetId")
        assert response.status_code == 200
        assert response.data == b"OK"