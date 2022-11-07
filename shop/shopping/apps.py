from django.apps import AppConfig


class ShoppingConfig(AppConfig):
    name = 'shopping'

    def ready(self):
        import shopping.signals
