from django.urls import path
from .views import UsersView, login_view

urlpatterns = [
    path("accounts/", UsersView.as_view()),
    path("login/", login_view),
]