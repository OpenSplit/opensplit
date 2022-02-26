from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.core.mail import send_mail
from django.core import mail


class User(AbstractUser):
    legacy_id = models.IntegerField(null=True)

    def __str__(self):
        return self.username

    def send_password_reset(self):
        context = {
            "base_url": settings.BASE_URL,
            "uid": urlsafe_base64_encode(force_bytes(self.pk)),
            "token": default_token_generator.make_token(self),
            "user": self,
        }
        subject = "Passwort zurücksetzen"
        html_message = render_to_string("email/password_reset.html", context)
        plain_message = render_to_string("email/password_reset.txt", context)
        from_email = "OpenSplit <app@opensplit.de"
        to = self.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
