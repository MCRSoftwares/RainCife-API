clean:
	@find . -name '*.pyc' -exec rm -f {} \;
	@find . -name 'Thumbs.db' -exec rm -f {} \;
	@find . -name '*~' -exec rm -f {} \;

requirements:
	@pip install -r requirements.txt

serve:
	@python manage.py serve

debug:
	@python manage.py debug

sync:
	@python manage.py sync

shell:
	@ipython --profile=raincife

setup:
	@ipython profile create raincife
	@IPYTHON=$$(ipython locate profile raincife); echo 'import raincife.apps' >> $$IPYTHON/startup/00_imports.py
