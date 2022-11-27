from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

from django.contrib.auth.models import User


# Create your views here.
def main(request):
    return render(request, 'index.html', {})


def registration(request):
    if request.method == 'GET':
        return render(request, 'helperAssistant/registration.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('loginuser')
            except IntegrityError as err:
                return render(request, 'helperAssistant/registration.html',
                              {'form': UserCreationForm(), 'error': 'Username is already exist'})

        else:
            return render(request, 'helperAssistant/registration.html',
                          {'form': UserCreationForm(), 'error': 'Password did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'helperAssistant/login.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'helperAssistant/login.html',
                          {'form': AuthenticationForm, 'error': 'Username or password didn\'t match'})
        else:
            login(request, user)
            return redirect('main')


def logoutuser(request):
    logout(request)
    return redirect('main')
