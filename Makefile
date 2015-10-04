
serve:
	@python manage.py runserver

requirements:
	@pip install -r requirements.txt

makemig:
	@python manage.py makemigrations

mig:
	@python manage.py migrate

sync:
	@python manage.py syncdb --noinput

static:
	@python manage.py collectstatic


init: requirements makemig sync
	$(info Creating superuser 'admin', please provide a password...)
	@python manage.py createsuperuser --username admin --email dummy@raincife.admin

crawl:
	@cd scrapy/ && scrapy crawl $(spider)

celery:
	@python manage.py celery -A raincife worker -l info

celery.beat:
	@python manage.py celerybeat --verbosity=2 --loglevel=DEBUG
