from django.apps import AppConfig

def ready(self):
    import accounts.signals

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

