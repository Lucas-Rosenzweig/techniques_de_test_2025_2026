test:
	@echo "Lancement des tests..."
	PYTHONPATH=src pytest -s

unit_test:
	@echo "Lancement des tests unitaires..."
	PYTHONPATH=src pytest tests/test_triangulator.py tests/test_api.py

perf_test:
	@echo "Lancement des tests de performance..."
	PYTHONPATH=src pytest tests/test_perf.py

coverage:
	@echo "Couverture du code"
	PYTHONPATH=src coverage run -m pytest --ignore=tests/test_perf.py tests/
	coverage report
	coverage html

lint:
	@echo "Analyse statique du code avec ruff"
	-ruff check src tests --fix
	ruff format src tests

doc:
	@echo "Génération de la documentation avec pdoc3"
#	On genère la doc uniquement pour les fichiers python principaux
	pdoc3 --html --output-dir docs --force src