from django.urls import path

from .views import (
    logout_,
    signin,
    signup
)


urlpatterns = [
    path('signin/', signin, name='signin'),
    path('logout/', logout_, name='logout'),
    path('signup/', signup, name='signup'),
]
