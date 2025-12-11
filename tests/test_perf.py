import time
import tracemalloc
from dataclasses import dataclass

import pytest

from classes.pointset import PointSet
from tests.services.pointsetService import generate_pointset


# Structure pour stocker les métriques de performance
@dataclass
class PerformanceMetrics:
    execution_time: float = 0.0
    cpu_time: float = 0.0
    memory_usage: int = 0


# Mesure de performance via un contexte 'with'
class PerformanceMonitor:
    """Classe qui gère le démarrage et l'arrêt du chronomètre
    et de la surveillance mémoire via le mot clé 'with'.
    """

    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.start_time = 0
        self.start_cpu = 0

    def __enter__(self):
        # Démarrage des compteurs au début du bloc 'with'
        tracemalloc.start()
        self.start_cpu = time.process_time()
        self.start_time = time.perf_counter()
        return self.metrics

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Arrêt des compteurs à la fin du bloc 'with'
        end_time = time.perf_counter()
        end_cpu = time.process_time()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Calcul des résultats
        self.metrics.execution_time = end_time - self.start_time
        self.metrics.cpu_time = end_cpu - self.start_cpu
        self.metrics.memory_usage = peak


@pytest.fixture
def performance_tracker():
    """Renvoie une instance du moniteur pour l'utiliser avec 'with'."""
    return PerformanceMonitor()


SIZES = [10, 100, 1000]  # 100000 peut être long, à tester
AMPLITUDES = [(0, 10), (0, 100), (0, 1000)]
AMPLITUDES_IDS = [f"{min}/{max}" for (min, max) in AMPLITUDES]
DISTRIBUTIONS = ["uniform", "linear", "clustered"]


@pytest.mark.parametrize("size", SIZES)
@pytest.mark.parametrize("amplitude", AMPLITUDES, ids=AMPLITUDES_IDS)
@pytest.mark.parametrize("distribution", DISTRIBUTIONS)
def test_triangulation_performance(size, amplitude, distribution, performance_tracker):
    # SETUP (Hors chrono)
    pointset = generate_pointset(size, amplitude, distribution)

    # ACTION (Mesurée)
    with performance_tracker as metrics:
        pointset.triangulate()

    print(f"\n{'-' * 60}")
    print(
        f" Triangulation Performance test- Size: {size}, Amplitude: {amplitude}, Distribution: {distribution}"
    )
    print(f"  > Time:   {metrics.execution_time:.6f} s")
    print(f"  > CPU Time:    {metrics.cpu_time:.6f} s")
    print(
        f"  > Peak Memory: {metrics.memory_usage / 1024:.2f} KB "
        f"({metrics.memory_usage / (1024 * 1024):.2f} MB)"
    )
    print(f"{'-' * 60}")

    # Eventuellement, on peut ajouter des assertions sur les métriques pour passer ou non le test de performance
    # assert metrics.execution_time < (size * 0.01)


@pytest.mark.parametrize("size", SIZES)
@pytest.mark.parametrize("amplitude", AMPLITUDES)
def test_pointset_to_bytes_performance(size, amplitude, performance_tracker):
    # SETUP (Hors chrono)
    pointset = generate_pointset(size, amplitude, "uniform")

    # ACTION (Mesurée)
    with performance_tracker as metrics:
        pointset.to_bytes()

    print(f"\n{'-' * 60}")
    print(f" Poinset to bytes Performance test- Size: {size}, Amplitude: {amplitude}")
    print(f"  > Time:   {metrics.execution_time:.6f} s")
    print(f"  > CPU Time:    {metrics.cpu_time:.6f} s")
    print(
        f"  > Peak Memory: {metrics.memory_usage / 1024:.2f} KB "
        f"({metrics.memory_usage / (1024 * 1024):.2f} MB)"
    )
    print(f"{'-' * 60}")

    # Eventuellement, on peut ajouter des assertions sur les métriques pour passer ou non le test de performance
    # assert metrics.execution_time < (size * 0.01)


@pytest.mark.parametrize("size", SIZES)
@pytest.mark.parametrize("amplitude", AMPLITUDES)
def test_pointset_from_bytes_performance(size, amplitude, performance_tracker):
    # SETUP (Hors chrono)
    pointset = generate_pointset(size, amplitude, "uniform")
    pointset_bytes = pointset.to_bytes()

    # ACTION (Mesurée)
    with performance_tracker as metrics:
        PointSet.from_bytes(pointset_bytes)

    print(f"\n{'-' * 60}")
    print(f" PointSetFromBytes Performance test- Size: {size}, Amplitude: {amplitude}")
    print(f"  > Time:   {metrics.execution_time:.6f} s")
    print(f"  > CPU Time:    {metrics.cpu_time:.6f} s")
    print(
        f"  > Peak Memory: {metrics.memory_usage / 1024:.2f} KB "
        f"({metrics.memory_usage / (1024 * 1024):.2f} MB)"
    )
    print(f"{'-' * 60}")

    # Eventuellement, on peut ajouter des assertions sur les métriques pour passer ou non le test de performance
    # assert metrics.execution_time < (size * 0.01)


@pytest.mark.parametrize("size", SIZES)
@pytest.mark.parametrize("amplitude", AMPLITUDES)
def test_triangles_to_bytes_performance(size, amplitude, performance_tracker):
    # SETUP (Hors chrono)
    pointset = generate_pointset(size, amplitude, "uniform")
    triangles = pointset.triangulate()

    # ACTION (Mesurée)
    with performance_tracker as metrics:
        triangles.to_bytes()

    print(f"\n{'-' * 60}")
    print(f" Triangles to bytes Performance test- Size: {size}, Amplitude: {amplitude}")
    print(f"  > Time:   {metrics.execution_time:.6f} s")
    print(f"  > CPU Time:    {metrics.cpu_time:.6f} s")
    print(
        f"  > Peak Memory: {metrics.memory_usage / 1024:.2f} KB "
        f"({metrics.memory_usage / (1024 * 1024):.2f} MB)"
    )
    print(f"{'-' * 60}")

    # Eventuellement, on peut ajouter des assertions sur les métriques pour passer ou non le test de performance
    # assert metrics.execution_time < (size * 0.01)
