from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", auth_views.LoginView.as_view(template_name="user/login.pug"), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
]
