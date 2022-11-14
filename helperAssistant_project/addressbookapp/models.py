
from django.db import models
from django.contrib.auth.models import User


class Phone(models.Model):
    phone = models.CharField(max_length=25, null=False)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['user_id', 'phone'], name='contact of user')
    #     ]

    def __str__(self):
        return f"{self.phone}:{self.user_id}"


class Contact(models.Model):

    name = models.CharField(max_length=25, null=False)
    birthday = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=150, null=False)

    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}:{self.user_id}"


class PhoneToContact(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)

