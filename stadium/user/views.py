from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import logout
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User has successfully registered")
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request,'user/register.html',{'form':form})

def profile(request):
    return render(request,'user/profile.html',{})


def logout(request):
    logout(request)
    return redirect('login')

