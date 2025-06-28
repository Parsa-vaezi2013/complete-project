from celery import shared_task

@shared_task
def send_welcome_email(user_id):
    print(f"به سایت ما خوش آمدید {user_id}")