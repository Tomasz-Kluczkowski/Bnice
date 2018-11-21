from django.apps import AppConfig
# from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    name = 'accounts'

    # def ready(self):
    #     from accounts.signals import populate_models
    #     post_migrate.connect(populate_models, sender=self)
