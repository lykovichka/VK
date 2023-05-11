from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import UserRegisterForm


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('account:user_account'))
    else:
        return render(request, 'registration/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            ins = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            ins.save()
            form.save_m2m()
            messages.success(request, 'Вы успешно зарегистрировались!')
            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'registration/reg.html', context)
