.PHONY: reproduce verify clean lint test

reproduce:
	python -m src.run_all --config config/config.yaml

verify:
	python -m src.utils.verify_manifest manifest.json

lint:
	flake8 src

test:
	pytest -q

clean:
	rm -rf artifacts/generated
