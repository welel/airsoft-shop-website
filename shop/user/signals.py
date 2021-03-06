from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer, User

@receiver(post_save, sender=User)
def create_customer(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        customer, created = Customer.objects.get_or_create(user=user)
        customer.save()
