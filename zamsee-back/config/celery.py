import os

from celery import Celery

# 공식 문서의 예제 코드

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config',
             # 브로커는 Redis 사용
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
