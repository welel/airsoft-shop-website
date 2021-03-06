from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    verbose_name = 'Profile'

    def ready(self):
        import user.signals
