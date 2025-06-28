from celery import shared_task

@shared_task
def procses_exchange(from_currency, to_currency, amount):
    print(f'درحال تبدیل {amount} {from_currency} به {to_currency}')
    return amount * 20


@shared_task
def beat_test_task():
    print("تسک زمان بندی انجام شده")