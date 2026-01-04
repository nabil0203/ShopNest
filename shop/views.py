from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RatingFrom, RegistrationForm, CheckoutForm

from .import models 

from django.db.models import Q, Min, Max, Avg



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
# 2 things-> Featured products | Shop by category

def home(request):
    featured_products = models.Product.objects.filter(available=True).order_by('-created_at')[:8]                   # Query set- 8 products in descending order
    categories = models.Category.objects.all()



    context = {
        'featured_products' : featured_products, 
        'categories' : categories
    }

    return render(request, '', context)







# Product List page
# 2 types of URL -> Normal URL | Category-wise
# This page has filtering options
# Filter based on 3 things -> Category || Price || Rating

def product_list(request, category_slug = None):
    category = None
    categories = models.Category.objects.all()
    products = models.Product.objects.all()


    # if category_slug exists filter then filter
    if category_slug:
        category = get_object_or_404(models.Category, category_slug)                                 # check whether the category_slug provided by the user, exists in the Category model
        product = products.filter(category = category)                                               # if it exists, then apply the filter; if not exists, give an error



    # Aggregate used to get a summary of the whole query set
    min_price = products.aggregate(Min('price'))['price__min']                               # calculating the 'minimum value' of the 'price' field from the all 'products' and storing it in the 'min_price' variable.
    max_price = products.aggregate(Max('price'))['price__max']                               # calculating the 'maximum value' of the 'price' field from the all 'products' and storing it in the 'max_price' variable.



    # filtering based on the 'min price'
    if request.GET.get('min_price'):
        products = products.filter(price__gte=request.GET.get('min_price'))
    

    # filtering based on the 'max price'
    if request.GET.get('max_price'):
        products = products.filter(price__lte=request.GET.get('max_price'))
    





