# Unit test for the triangulator api
from unittest.mock import Mock, patch
from urllib.error import HTTPError

import pytest

from classes.pointset import Point, PointSet
from Triangulator import app as flask_app


# Helper pour avoir un PointSetValide
def get_valid_pointset() -> PointSet:
    return PointSet([Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0)])


# Mock le chemin pour urlopen de urllib afin d'éviter les appels réseau réels
URLOPEN_PATH = "urllib.request.urlopen"


class TestTriangulatorApi:
    # Fixture for flask client
    @pytest.fixture
    def client(self):
        flask_app.config["TESTING"] = True
        with flask_app.test_client() as client:
            yield client

    def test_api_200_triangulation_ok(self, client):
        # Préparation des données du mock :
        valid_point_set = get_valid_pointset()
        valid_point_set_bytes = valid_point_set.to_bytes()
        expected_triangles = valid_point_set.triangulate()

        # Mock du call API vers le PointSetManager
        mock_response = Mock()
        mock_response.read.return_value = valid_point_set_bytes
        mock_response.getcode.return_value = 200
        mock_response.status = 200  # Sécurité dans le cas ou getcode n'est pas utilisé dans ma future implémentation
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        with patch(URLOPEN_PATH, return_value=mock_response):
            response = client.get("/triangulation/123e4567-e89b-12d3-a456-426614174000")
            assert response.status_code == 200
            assert response.content_type == "application/octet-stream"
            assert response.data == expected_triangles.to_bytes()

    def test_api_400_invalid_pointset_id(self, client):
        invalid_id = "NotAValidUUID"
        response = client.get(f"/triangulation/{invalid_id}")
        assert response.status_code == 400
        assert response.content_type == "application/json"

    def test_api_404_pointset_not_found(self, client):
        valid_uuid = "123e4567-e89b-12d3-a456-426614174000"

        # Mock du call API qui retourne une erreur 404
        mock_http_error = HTTPError(
            url=f"http://localhost:5000/pointset/{valid_uuid}",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=None,
        )

        with patch(URLOPEN_PATH, side_effect=mock_http_error):
            response = client.get(f"/triangulation/{valid_uuid}")
            assert response.status_code == 404
            assert response.content_type == "application/json"

    def test_api_500_triangulation_algorithm_error(self, client):
        valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
        valid_point_set = get_valid_pointset()
        valid_point_set_bytes = valid_point_set.to_bytes()

        # Mock du call API réussi
        mock_response = Mock()
        mock_response.read.return_value = valid_point_set_bytes
        mock_response.getcode.return_value = 200
        mock_response.status = 200
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        with patch(URLOPEN_PATH, return_value=mock_response):
            # Mock de la méthode triangulate pour simuler une erreur interne
            with patch.object(
                PointSet, "triangulate", side_effect=ValueError("Triangulation error")
            ):
                response = client.get(f"/triangulation/{valid_uuid}")
                assert response.status_code == 500
                assert response.content_type == "application/json"

    def test_api_503_manager_communication_error(self, client):
        valid_uuid = "123e4567-e89b-12d3-a456-426614174000"

        # Mock du call API qui lève une exception réseau (timeout, connection error)
        with patch(URLOPEN_PATH, side_effect=ConnectionError("Network timeout")):
            response = client.get(f"/triangulation/{valid_uuid}")
            assert response.status_code == 500
            assert response.content_type == "application/json"
