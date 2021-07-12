from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("password-reset", views.password_reset, name="trigger-password-reset"),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(template_name="user/password-reset-confirm.pug"),
        name="password_reset_confirm",
    ),
    path(
        "reset/done",
        auth_views.PasswordResetCompleteView.as_view(template_name="user/password-reset-complete.pug"),
        name="password_reset_complete",
    ),
    path("register", views.register, name="register"),
    path("login", auth_views.LoginView.as_view(template_name="user/login.pug"), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
]
