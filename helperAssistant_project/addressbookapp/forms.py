from django import forms
from datetime import date
from .models import Contact, Phone, Email


class ContactForm(forms.ModelForm):
    name = forms.CharField(label='Имя')
    birthday = forms.DateField(label='День рождения', widget=forms.widgets.SelectDateWidget())
    address = forms.CharField(label='Адресс')
    description = forms.CharField(label='Описание')

    class Meta:
        model = Contact
        fields = ['name', 'birthday', 'address', 'description']


class PhoneForm(forms.ModelForm):
    phone = forms.IntegerField(label='Телефон')

    class Meta:
        model = Phone
        fields = ['phone', ]


class EmailForm(forms.ModelForm):
    phone = forms.IntegerField(label='Email')

    class Meta:
        model = Email
        fields = ['email', ]


class ContactEditForm(forms.Form):
    name = forms.CharField(label='Имя')
    birthday = forms.DateField(label='День рождения', widget=forms.widgets.SelectDateWidget())
    email = forms.EmailField(label='Электронная почта', widget=forms.widgets.EmailInput())
    description = forms.CharField(label='Описание')

