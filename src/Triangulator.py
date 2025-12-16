"""Triangulator API Service.

This module provides a Flask API to triangulate a PointSet retrieved from
a PointSet Manager service.
"""

import urllib.error
import urllib.request
import uuid

from flask import Flask, Response, jsonify

from classes.pointset import PointSet

app = Flask(__name__)


@app.route("/triangulation/<string:pointSetId>", methods=["GET"])
def triangulation(pointSetId: str):
    """Retrieve a PointSet by ID and return its triangulation.

    Args:
        pointSetId (str): The UUID of the PointSet to triangulate.

    Returns:
        Response: The triangulated Triangles as bytes or an error message.

    """
    # Valide l'id du pointset
    try:
        uuid.UUID(pointSetId)
    except ValueError:
        return jsonify({"error": "Invalid UUID"}), 400

    try:
        # Récupère le pointset depuis le pointset manager en partant du principe
        # que le pointset manager est en localhost:5000
        url = f"http://localhost:5000/pointset/{pointSetId}"
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:
                point_set_bytes = (
                    response.read()
                )  # Récupère le pointset sous forme de bytes
                point_set = PointSet.from_bytes(
                    point_set_bytes
                )  # Transforme les bytes en pointset

                try:
                    triangles = point_set.triangulate()  # Triangule le pointset
                    return Response(
                        triangles.to_bytes(),  # Transforme les triangles en bytes
                        # Indique que le contenu est en bytes
                        mimetype="application/octet-stream",
                        status=200,
                    )
                except ValueError as e:
                    return jsonify(
                        {"error": str(e)}
                    ), 500  # Retourne une erreur si la triangulation echoue
            else:
                # Retourne une erreur si le pointset n'est pas trouvé
                return jsonify(
                    {"error": "Failed to retrieve PointSet"}
                ), response.getcode()

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return jsonify({"error": "PointSet not found"}), 404
        return jsonify({"error": str(e)}), 500
    except (urllib.error.URLError, ConnectionError):
        return jsonify({"error": "Service unavailable"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
