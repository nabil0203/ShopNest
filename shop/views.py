from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RatingFrom, RegistrationForm, CheckoutForm

from .import models



# Create your views here.



# manual Authentication
def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request, user)
            redirect('')
        else:
            messages.error(request,"Invalid Credentials")


    else:
        return render(request, '')        






# register new user
def register_view(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successful!")
            return redirect('')
        
    else:
        form = RegistrationForm()
    
    return render(request, '', {'form' : form})





# user logout
def logout_view(request):
    logout(request)
    return render ('')






# Home page
# 2 things-> Featured products || Shop by category

def home(request):
    featured_products = models.Product.objects.filter(available=True).order_by('-created_at')[:8]                   # descending order




