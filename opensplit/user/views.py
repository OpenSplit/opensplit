from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, PasswordResetForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect("index")

    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Anmeldung erfolgreich. Du kannst dich jetzt einloggen.")
            return redirect("login")

    return render(request, "user/register.pug", {"form": form})


def password_reset(request):
    if request.user.is_authenticated:
        return redirect("index")

    form = PasswordResetForm()
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Falls es einen Account mit dieser Addresse gab, haben wir dir eine EMail geschickt")
            try:
                user = User.objects.get(email=form.cleaned_data["email"])
            except User.DoesNotExist:
                return redirect("login")
            user.send_password_reset()
            return redirect("login")

    return render(request, "user/trigger-password-reset.pug", {"form": form})
