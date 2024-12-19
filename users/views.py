from django import forms
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterUserForm


def login_user(request):
    if request.method == "POST":
        username=request.POST["email"]
        password=request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.success(request,("There was an error, try again")) 
    return render(request, "authenticate/login.html")

def logout_view(request):
    logout(request)
    return redirect('/accounts/login')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request, "Неверный логин или пароль")
    else:
        form = RegisterUserForm()

    return render(request, "authenticate/register_user.html", {"form":form})

