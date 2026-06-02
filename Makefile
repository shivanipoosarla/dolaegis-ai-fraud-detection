.PHONY: demo test check api dashboard clean

demo:
	PYTHONPATH=src python -m dolaegis.cli --input data/sample_transactions.csv --outdir reports

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

check:
	python -m compileall src tests
	PYTHONPATH=src python -m unittest discover -s tests -v

api:
	PYTHONPATH=src uvicorn dolaegis.api:app --reload

dashboard:
	PYTHONPATH=src python -m dolaegis.cli --input data/sample_transactions.csv --outdir reports
	@echo "Open reports/fraud_dashboard.html in a browser."

clean:
	rm -f reports/fraud_risk_report.md reports/fraud_risk_report.json reports/fraud_dashboard.html reports/audit_log.jsonl
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
