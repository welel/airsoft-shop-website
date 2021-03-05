from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Customer
from main.models import Cart
from main.utils import set_cookie


@transaction.atomic
def signup(request):
    """Handles an user registration page."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer = Customer.objects.create(user=user)
            cart = Cart.objects.get(pk=request.COOKIES['cart_id'])
            cart.owner = customer
            cart.save(update_fields=['owner'])
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@transaction.atomic
def signin(request):
    """Handles a login page."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            anon_cart = Cart.objects.get(pk=request.COOKIES['cart_id'])
            customer = Customer.objects.get(user=user)
            cart = Cart.objects.get(owner=customer, in_order=False)
            if anon_cart != cart:
                anon_cart.delete()
            response = HttpResponseRedirect(reverse('index'))
            set_cookie(response, 'cart_id', cart.pk)
            login(request, user)
            return response
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})


@login_required()
def logout_(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
