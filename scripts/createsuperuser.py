"""Creation of superuser and ``Cart`` for superuser.

After creation of a superuser with manage.py you must create a cart
in database and link it with a custmer to use admin CRUD.

"""
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")
sys.path.append('../shop')

import django
django.setup()

from django.contrib.auth import get_user_model

from user.models import Customer
from shopping.models import Cart

User = get_user_model()


if __name__ == '__main__':
    username = input('Username: ')
    email = input('Email: ')
    password = input('Password: ')
    superuser = User.objects.create_superuser(username, email, password)
    customer = Customer.objects.get(user=superuser)
    cart = Cart.objects.create(owner=customer)
