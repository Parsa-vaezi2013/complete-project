from django.core.management.base import BaseCommand
from django.core.management import call_command
from exchange.utils import get_dollar_price_from_nobitex

class Command(BaseCommand):
    help = 'مایگریشن کردن و آپدیت کردن قیمت بعدش هم ران سرور'

    def handle(self, *args, **options):
        self.stdout.write("مایگریشن ران میشود")
        call_command("migrate")
        self.stdout.write("مایگریشن با موفقیت انجام شد")
        self.stdout.write("حالا میریم قیمت دلار رو آپدیت کنیم")


        price = get_dollar_price_from_nobitex()
        if price:
            self.stdout.write(f"قیمت گرفته شده از نوبیتکس: {price}")

        else:
            self.stdout.write("خاک تو سر نوبیتکس، قیمتو نداد :(")

        self.stdout.write("حالا بریم برای ران سرور")
        call_command("runserver")
        self.stdout.write("اینم تموم شد")
