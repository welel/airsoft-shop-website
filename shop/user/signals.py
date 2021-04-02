from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from .models import Customer, User
from .utils import send_activation_notification


@receiver(post_save, sender=User)
def create_customer(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        customer, created = Customer.objects.get_or_create(user=user)
        customer.save()


user_registered = Signal(providing_args=['instance'])

@receiver(user_registered)
def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])
