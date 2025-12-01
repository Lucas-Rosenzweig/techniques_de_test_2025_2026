test:
	@echo "Lancement des tests..."
	pytest -s

unit_test:
	@echo "Lancement des tests unitaires..."
	pytest tests/test_triangulator.py tests/test_api.py

perf_test:
	@echo "Lancement des tests de performance..."
	pytest tests/test_perf.py

coverage:
	@echo "Couverture du code"
	-coverage run -m pytest > /dev/null 2>&1
	coverage report
	coverage html
