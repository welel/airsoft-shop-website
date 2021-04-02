from django.urls import path

from .views import (
    edit_user,
    logout_,
    signin,
    signup,
    RegisterDoneView,
    user_activate
)


urlpatterns = [
    path('signin/', signin, name='signin'),
    path('logout/', logout_, name='logout'),
    path('signup/', signup, name='signup'),
    path('edit_user/', edit_user, name='edit_user'),
    path('register_done/', RegisterDoneView.as_view(),
         name='register_done'),
    path('user_activate/<str:sign>', user_activate,
         name='register_activate')
]
