from django import forms
from datetime import date
from .models import Contact, Phone


class ContactForm(forms.ModelForm):
    name = forms.CharField(label='Имя')
    birthday = forms.DateField(label='День рождения', widget=forms.widgets.SelectDateWidget())
    email = forms.EmailField(label='Электронная почта', widget=forms.widgets.EmailInput())
    description = forms.CharField(label='Описание')

    class Meta:
        model = Contact
        fields = ('name', 'birthday', 'email', 'description')


class ContactEditForm(forms.Form):
    name = forms.CharField(label='Имя')
    birthday = forms.DateField(label='День рождения', widget=forms.widgets.SelectDateWidget())
    email = forms.EmailField(label='Электронная почта', widget=forms.widgets.EmailInput())
    description = forms.CharField(label='Описание')

