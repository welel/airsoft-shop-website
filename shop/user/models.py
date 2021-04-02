from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Customer(models.Model):
    """Profile of registered client of the store.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='user')
    phone = models.CharField(max_length=20, blank=True, default='')
    address = models.CharField(max_length=1024, blank=True, default='')

    def __str__(self):
        return 'User: {}'.format(self.user.username)
