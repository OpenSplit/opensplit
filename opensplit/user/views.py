from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from .forms import RegisterForm, LoginForm
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
