from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, PasswordResetForm
from .models import User


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "You registered successfully. You can log in now")
            return redirect("login")

    return render(request, "user/register.pug", {"form": form})


def password_reset(request):
    form = PasswordResetForm()
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data["email"])
            except User.DoesNotExist:
                return redirect("login")
            user.send_password_reset()
            return redirect("login")

    return render(request, "user/trigger-password-reset.pug", {"form": form})
