from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db import connection
connection.queries


class Contact(models.Model):

    name = models.CharField(max_length=25, null=False)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=150, null=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # def __str__(self):
    #     return f"{self.id}***{self.name}***{self.birthday}***{self.address}***{self.description}:"


class Phone(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='phones')

    phone = models.CharField(max_length=150, null=False)


class Email(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='emails')

    email = models.EmailField(max_length=100, null=False)
