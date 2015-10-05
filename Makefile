
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

shell:
	@python manage.py shell

crawl:
	@cd scrapy/ && scrapy crawl $(spider)

celery:
	@python manage.py celery -A raincife worker -l info

celery.beat:
	@python manage.py celerybeat --verbosity=2 --loglevel=DEBUG

celery.start:
	@supervisorctl tail celery
	@supervisorctl start celery

celery.beat.start:
	@supervisorctl tail celerybeat
	@supervisorctl start celerybeat

celery.stop:
	@supervisorctl stop celery

celery.beat.stop:
	@supervisorctl stop celerybeat

celery.restart:
	@supervisorctl restart celery

celery.beat.restart:
	@supervisorctl restart celerybeat

scrapy.install:
	@sudo pip install scrapy

redis.install:
	# NOTE: ONLY WORKS IF YOU'RE USING VAGRANT
	@cd /home/vagrant/.redis/redis-3.0.4/utils/ && sudo ./install_server.sh

redis.start:
	@sudo service redis_6379 start

redis.stop:
	@sudo service redis_6379 stop

redis.restart:
	@sudo service redis_6379 restart

services.start: redis.start celery.start celery.beat.start

services.stop: celery.stop celery.beat.stop redis.stop

services.restart: redis.restart celery.restart celery.beat.restart
