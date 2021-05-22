from django.urls import path
from . import views

urlpatterns = [
    path("login", views.LoginAPIView.as_view(), name="login"),
    path("register", views.RegistrationAPIView.as_view(), name="register"),
]
