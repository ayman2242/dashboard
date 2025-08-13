from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm 

# Create your views here.
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username , password= password)
            if user:
                login(request,user)
                return redirect('home')
            else:
                form.add_error(None, "incalid username or password")
    else:
        form = LoginForm()

    return render(request,'login.html',{'form':form})

def logout_page(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request,"home.html")
