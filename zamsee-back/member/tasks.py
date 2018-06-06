from django.core.mail import send_mail

from config import celery_app


# ignore_result = task에 결과를 저장하지 않는 옵션, 성능 향상
@celery_app.task(bind=True, ignore_result=True)
def send_mail_task(self, subject, message, from_email, recipient):
    send_mail(
        subject=subject,
        message='Activate email',
        html_message=message,
        from_email=from_email,
        recipient_list=[
            recipient
        ],
    )
