from django.core.signing import BadSignature
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.urls import reverse

from .forms import UserForm
from .models import Customer, User
from .signals import user_registered
from .utils import signer
from shopping.models import Cart
from shopping.utils import set_cookie


@transaction.atomic
def signup(request):
    """Handles an user registration page."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = user.username
            # TODO: put is active in customer
            user.is_active = False
            user.save(update_fields=['email', 'is_active'])
            customer = Customer.objects.get(user=user)
            cart = Cart.objects.get(pk=request.COOKIES['cart_id'])
            cart.owner = customer
            cart.save(update_fields=['owner'])
            login(request, user)
            user_registered.send(UserCreationForm, instance=user)
            return HttpResponseRedirect(reverse('register_done'))
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


@login_required()
def edit_user(request):
    user = request.user
    user_form = UserForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(
        User, Customer, fields=('phone', 'address')
    )
    formset = ProfileInlineFormset(instance=user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        formset = ProfileInlineFormset(request.POST, instance=user)

        if user_form.is_valid():
            created_user = user_form.save(commit=False)
            formset = ProfileInlineFormset(request.POST, instance=created_user)

            if formset.is_valid():
                created_user.save()
                formset.save()
                return HttpResponseRedirect(reverse('index'))

    return render(request, "edit_user.html", {
        "noodle": user.pk,
        "noodle_form": user_form,
        "formset": formset,
    })


class RegisterDoneView(TemplateView):
    template_name = 'user/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        user = request.user
        customer = Customer.objects.get(user=user)
        user.delete()
        customer.delete()
        return render(request, 'user/bad_signature.html')
    user = get_object_or_404(User, username=username)
    if user.is_active:
        template = 'user/user_is_activated.html'
    else:
        template = 'user/activation_done.html'
        user.is_active = True
        user.save()
        login(request, user)
    return render(request, template)
