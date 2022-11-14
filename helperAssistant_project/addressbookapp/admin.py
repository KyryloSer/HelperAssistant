from django.contrib import admin
from .models import Phone, Contact, PhoneToContact

# Register your models here.
admin.site.register(Phone)
admin.site.register(Contact)
admin.site.register(PhoneToContact)
