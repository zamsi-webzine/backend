import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config',
             broker='redis://zamsee-redis.sgm0ct.ng.0001.apn2.cache.amazonaws.com:6379',
             backend='redis://zamsee-redis.sgm0ct.ng.0001.apn2.cache.amazonaws.com:6379')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
