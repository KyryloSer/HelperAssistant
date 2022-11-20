from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):

    name = models.CharField(max_length=25, null=False)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=150, null=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    # def __str__(self):
    #     return f"{self.id}***{self.name}***{self.birthday}***{self.address}***{self.description}:"


class Phone(models.Model):
    phone = models.CharField(max_length=50, null=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)


class Email(models.Model):
    email = models.EmailField(max_length=25, null=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
