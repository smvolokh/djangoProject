from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Rifle, Skin
from .forms import LoginForm, RegistrationForm



def get_rifle_list(request):
    rifles = Rifle.objects.order_by('title')
    if request.user.is_authenticated:
        name = request.user.username
    else:
        name = 'Guest'
    context = {'data': rifles, 'name': name}
    return render(request, 'csgo/rifle_list.html', context)


def log_out(request):
    logout(request)
    redirect_url = request.GET.get('next') or reverse('index')
    return redirect(redirect_url)


def log_in(request):
    if request.method == 'POST':
        logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET['next'])
            else:
                form.add_error('Invalid credentials!')
    else:  # GET
        form = LoginForm()
    return render(request, 'csgo/login.html', {'form': form})


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



def rifle(request, name):
    if request.method == 'POST':
        return create_skin(request, name)
    else:
        return render_rifle(request, name)


def render_rifle(request, name, add_context=None):
    if add_context is None:
        add_context = {}
    rifle = get_object_or_404(Rifle, title=name)
    skins = rifle.skin_set.all()
    context = {'title': rifle.title,
               'skins': skins.order_by('subject'),
               **add_context
               }
    return render(request, 'csgo/rifles.html', context)

@login_required(login_url='login')
def create_skin(request, name):
    rifle = get_object_or_404(Rifle, title=name)

    skin = request.POST['skin']
    skin_error = None
    if not skin or skin.isspace():
        skin_error = 'Empty subject!'

    text = request.POST['text']
    text_error = None
    if not text or text.isspace():
        text_error = 'Empty text!'

    if skin_error or text_error:
        error_context = {
            'skin_error': skin_error,
            'text_error': text_error,
            'skin': skin,
            'text': text
        }
        return render_rifle(request, rifle.title, error_context)
    else:
        rifle.skin_set.create(subject=skin, text=text)
        return HttpResponseRedirect(reverse('rifle_by_name', kwargs={'name': rifle.title}))
