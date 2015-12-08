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
