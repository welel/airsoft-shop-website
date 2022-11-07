import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from shopping.models import Order


@receiver(post_save, sender=Order)
def calculate_arrival_date(sender, instance, **kwargs):
    if not instance.receiving_date:
        # Here we should calculate arrival date based on data
        # that we have about our delivery system.
        # Scince we don't have a delivery system,
        # we just set deafult arrival time.
        # arrival time = order date + week.
        instance.receiving_date = datetime.date.today() + \
                               datetime.timedelta(days=7)
        instance.save()
