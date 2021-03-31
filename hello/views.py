from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from csgo.views import get_rifle_list
from .forms import LoginForm, RegistrationForm


@login_required(login_url='/hello/login')
def index(request):
    if request.user.is_authenticated:
        name = request.user.username
    else:
        name = 'Guest'
    return render(request, 'hello/hello.html', {'name': name})


def log_in(request):
    if request.method == 'POST':
        logout(request)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'])
        else:
            error = 'Invalid credentials!'
    else: # GET
        error = None
    return HttpResponse(render(request, 'hello/login.html', {'error': error}))

def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            logout(request)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            check_password = form.cleaned_data['check_password']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'User already exists!')
            elif password != check_password:
                form.add_error('check_password', 'Passwords mismatch!')
            else:
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password)
                login(request, user)
                return redirect('../hello')
    else:
        form = RegistrationForm()
    return render(request, 'csgo/signup.html', {'form': form})