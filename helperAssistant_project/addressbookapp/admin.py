from django.contrib import admin
from .models import Contact, Phone, Email

# Register your models here.
admin.site.register(Phone)
admin.site.register(Contact)
admin.site.register(Email)
