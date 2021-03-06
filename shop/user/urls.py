from django.urls import path

from .views import (
    edit_user,
    logout_,
    signin,
    signup
)


urlpatterns = [
    path('signin/', signin, name='signin'),
    path('logout/', logout_, name='logout'),
    path('signup/', signup, name='signup'),
    path('edit_user/', edit_user, name='edit_user')
]
