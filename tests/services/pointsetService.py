import random

from pygments.lexer import default

from classes.pointset import PointSet, Point


def generate_pointset(size, amplitude, distribution) -> PointSet:
    min_val, max_val = amplitude
    points = []

    match distribution:
        case "uniform":
            # Génère des points de manière uniforme
            points = [Point(random.uniform(min_val, max_val), random.uniform(min_val, max_val)) for _ in range(size)]
        case "linear":
            # Génère des points de manière linéaire entre min_val et max_val avec y = ax + b + un peu de bruit
            points = [Point(x, x * 1.5 + random.uniform(-1, 1))for x in [random.uniform(min_val, max_val) for _ in range(size)]]
        case "clustered":
            # Création de quelques centres
            centers = [(random.uniform(min_val, max_val), random.uniform(min_val, max_val)) for _ in range(5)]
            for _ in range(size):
                cx, cy = random.choice(centers)
                # Ajout d'un offset au hasard autour du centre choisi pour créer un cluster
                points.append(Point(cx + random.gauss(0, (max_val - min_val) / 20),
                                   cy + random.gauss(0, (max_val - min_val) / 20)))
        case _:
            raise ValueError(f"Unknown distribution type: {distribution}")

    return PointSet(points)
