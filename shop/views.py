from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RatingForm, RegistrationForm, CheckoutForm

from . import models 

from django.db.models import Q, Min, Max, Avg

from . import forms

from .sslcommerz import generate_sslcommerz_payment, send_order_confirmation_email

from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt



# manual Authentication
def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials")

    else:
        return render(request, 'shop/login.html')        






# register new user
def register_view(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successful!")
            return redirect('home')
    else:
        form = RegistrationForm()
    
    return render(request, 'shop/register.html', {'form' : form})





# user logout
def logout_view(request):
    logout(request)
    return redirect('login')






# Home page
# 2 things-> Featured products | Shop by category

def home(request):
    featured_products = models.Product.objects.filter(available=True).order_by('-created_at')[:8]                   # Query set- 8 products in descending order
    categories = models.Category.objects.all()



    context = {
        'featured_products' : featured_products, 
        'categories' : categories
    }

    return render(request, 'shop/home.html', context)







# All Product List page

# 2 types of URL -> Normal URL | Category-wise URL
# This page has filtering options
# Filter based on 3 things -> Category || Price || Rating

def product_list(request, category_slug = None):
    category = None
    categories = models.Category.objects.all()
    products = models.Product.objects.all()


    # filtering based on the 'category'
    if category_slug:
        category = get_object_or_404(models.Category, slug = category_slug)                                 # check whether the category_slug provided by the user, exists in the Category model
        products = products.filter(category = category)                                               # if it exists, then apply the filter; if not exists, give an error



    # Aggregate used to get a summary of the whole query set
    min_price = products.aggregate(Min('price'))['price__min']                                  # calculating the 'minimum value' of the 'price' field from the all 'products' and storing it in the 'min_price' variable.
    max_price = products.aggregate(Max('price'))['price__max']                                  # calculating the 'maximum value' of the 'price' field from the all 'products' and storing it in the 'max_price' variable.



    # filtering based on the 'min price'
    if request.GET.get('min_price'):
        products = products.filter(price__gte = request.GET.get('min_price'))                              # gte = greater than equal; if the price is grater equal to the user's min price
    

    # filtering based on the 'max price'
    if request.GET.get('max_price'):
        products = products.filter(price__lte = request.GET.get('max_price'))                               # lte = less than equal; if the price is less equal to the user's max price



    # filtering based on the 'rating'
    if request.GET.get('rating'):

        min_rating = request.GET.get('rating')
       
        products = products.annotate(
            avg_rating = Avg('ratings__rating')
            ).filter(avg_rating__gte=min_rating)


        # 1. A temporary field named 'avg_rating' is created [needed this temp variable bcz in the Product Model there is no method/variable to calculate this AVG]
        # 2. annotate() adds this 'avg_rating' field to each product
        # 3. The average rating is calculated for each individual product
        # 4. Aggregation (AVG) is applied on the rating field
        # 5. For each product, the 'rating' value is accessed using the related_name 'ratings' from the Rating model
        # 6. Products are filtered where avg_rating is greater than or equal ---> to the user-selected rating





    # search
    if request.GET.get('search'):

        query = request.GET.get('search')

        products = products.filter(
            Q(name__icontains = query) | 
            Q(description__icontains = query) | 
            Q(category__name__icontains = query)  
        )




    context = {
        'category' : category,
        'categories' : categories,
        'products' : products,
        'min_price' : min_price,
        'max_price' : max_price
    }

    return render(request, 'shop/product_list.html', context)
    





    



# Single product details page

def product_detail(request, slug):
    product = get_object_or_404(models.Product, slug = slug, available = True)                                                      # comparing product's slug with the user's provided product slug
    related_products = models.Product.objects.filter(category = product.category).exclude(id = product.id)                           # related_product == all products from the same category of the current product
                                                                                                                                    # exclude == Excludes the product that is currently being viewed

    user_rating = None


    if request.user.is_authenticated:
        try:
            user_rating = models.Rating.objects.get(product=product, user=request.user)                                         # if the user is authenticated, then the rating of that user is stored in "user_rating" and show in the details page
        except models.Rating.DoesNotExist:
            pass 

    
    #-----handle without try-except exception---------
    # if request.user.is_authenticated:
    #     user_rating = models.Rating.objects.filter(product=product, user=request.user).first()
    
    #     if user_rating:
    #         # The rating exists, you can use it
    #         pass
    #     else:
    #         # No rating found
    #         pass


    rating_form = RatingForm(instance= user_rating)



    context = {
        'product' :product,
        'related_products' : related_products,
        'user_rating' : user_rating,
        'rating_form' : rating_form
    }


    return render(request, 'shop/product_detail.html', context)









# Rate a Product 
# user can rate when--> i)logged in user, ii) Purchased the product

@login_required
def rate_product(request, product_id):
    product = get_object_or_404(models.Product, id = product_id)                                        # get the specific product


    # filtering the product if it is purchased by the user or not
    ordered_items = models.OrderItem.objects.filter(
        order__user = request.user,
        product = product,
        order__paid = True
    )



    # If the user did not order the product, can't rate
    if not ordered_items.exists():
        messages.warning(request, 'You can only rate products you have purchased!')

        return redirect('product_detail', slug=product.slug)
    



    # has rating or not
    try:
        rating = models.Rating.objects.get(product=product, user = request.user)                            # User already rated once, system will not allow to rate again

    except models.Rating.DoesNotExist:                                                                      # no rating
        rating = None





    # rating form
    # If already has rating --> rating form will be filled with that rating and can update the rating -->> instance = user rating
    # If not rated --> can give rating -->> instance = NONE

    if request.method == 'POST':
        form = RatingForm(request.POST, instance = rating) 
        
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product
            rating.user = request.user 
            rating.save()
            return redirect('product_detail', slug=product.slug)


    else:
        form = RatingForm(instance=rating)

    

    context = {
        'form' : form,
        'product' : product
    }


    return render(request, 'shop/rate_product.html', context)









# Everything about Cart - feature


# cart details
@login_required
def cart_detail(request):

    # user don't have any cart
    try:
        cart = models.Cart.objects.get(user=request.user)

    # user have any cart
    except models.Cart.DoesNotExist:
        cart = models.Cart.objects.create(user=request.user)
    



    return render(request, 'shop/cart.html', {'cart' : cart})







# cart add
# 1 user -> 1 cart
@login_required
def cart_add(request,product_id):
    product = get_object_or_404(models.Product, id = product_id)


    # Check cart exists or not (exception handling)
    try:
        cart = models.Cart.objects.get(user = request.user)                                    # if the user already have a cart, then put that in the "cart" variable

    except models.Cart.DoesNotExist:                                                              # if the user do not have a cart,
        cart = models.Cart.objects.create(user = request.user)                                    # then create one


    
    # add items into cart
    try:
        cart_item = models.CartItem.objects.get(cart=cart, product=product)                                   # if the item is already in the cart
        # Check if adding 1 more unit exceeds stock
        if cart_item.quantity >= product.stock:
            messages.warning(request, f"Cannot add more {product.name}. Only {product.stock} in stock!")
        else:
            cart_item.quantity += 1                                                                               # then just increase the quantity
            cart_item.save()
            messages.success(request, f"{product.name} has been added to your cart!")


    except models.CartItem.DoesNotExist:                                                                   # if the item is not in the cart(empty cart)
        models.CartItem.objects.create(cart=cart, product = product, quantity = 1)                         # then add the item in the cart; initial item quantity = 1
        messages.success(request, f"{product.name} has been added to your cart!")

    return redirect('product_detail', slug=product.slug)





    


# cart update
# cart item increase/decrease
@login_required
def cart_update(request,product_id):
    
    cart = get_object_or_404(models.Cart, user=request.user)                                                    # which cart [user's cart exists or not]

    product = get_object_or_404(models.Product, id=product_id)                                                     # main product which is in the cart as cart item

    cart_item = get_object_or_404(models.CartItem, cart=cart, product=product)                                  # cart item[the item we are working with]

    quantity = int(request.POST.get('quantity', 1))                                                               # initial quantity = 1                       


   
    # Check stock validation
    if quantity > product.stock:
        messages.warning(request, f"Cannot add {quantity} items. Only {product.stock} in stock!")
        quantity = product.stock  # Set to max available stock


    # user, soap -> 5, 4, 3, 2, 1, 0
    # when '0' piece it means we need to delete the cartitem
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, f"{product.name} has been removed from your cart!")
    
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"Cart updated successfully!!")



    return redirect('cart_detail')








# full cart delete
@login_required
def cart_remove(request,product_id):

    # to delete, at first we need to get the following things
    cart = get_object_or_404(models.Cart, user=request.user)
    product = get_object_or_404(models.Product, id=product_id)
    cart_item = get_object_or_404(models.CartItem, cart=cart, product=product)


    # delete
    cart_item.delete()
    messages.success(request, f"{product.name} has been Deleted from your cart!")



    return redirect('cart_detail')











# Checkout
# 1. take data from the cart
# 2. Input all the data of CheckoutForm: ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city','note']
# 3. show full amount
# 4. Payment gateway
# full transition:- Product --> Cart Item --> Order Item

@csrf_exempt                                                                    # to secure payment related workflow
@login_required
def checkout(request):

    try:
        cart = models.Cart.objects.get(user=request.user)                                # user have a cart(cart has items)
        if not cart.items.exists():                                                      # suppose deleted the items until the cart is 'empty'
            messages.warning(request, 'Your cart is empty')                              # as the cart is empty, so it will not go to checkout page----> it will show a warning message
            return redirect('cart_detail')

    
    except models.Cart.DoesNotExist:                                                 # user have no cart
        messages.warning(request, 'Your cart is empty!')                             # as there is no cart, so it will never go to checkout page----> it will show a warning message
        return redirect('cart_detail')
    


    # user have a cart (cart has items)
    # CheckoutForm fill-up (means inserting data into the form)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)                                         # "commit=False"--> form object created but not pushed in the DB
            order.user = request.user
            order.save()                                        # save means -> order done


            for item in cart.items.all():
                models.OrderItem.objects.create(                                # creating OrderItem for all objects
                    order = order,
                    product = item.product,                                     # here, cart item = order item
                    price = item.product.price,                                 # product's main price = order item's main price
                    quantity = item.quantity                                    # cart item's quantity = order item's quantity
                )

            
            # order done finally
            # As the order is completed, the cart will not has any value
            cart.items.all().delete() 
            request.session['order_id'] = order.id                                          # session delete
            return redirect('payment_process')

    else:
        form = forms.CheckoutForm()

     
    context = {
        'cart' : cart,
        'form' : form
    }


    return render(request,'shop/checkout.html', context)



        





# Payment
# 4 Steps



# 0. Payment Process
# We Need SSL Commerz

@csrf_exempt
@login_required
def payment_process(request):

    # session id used to get the information of the order

    order_id = request.session.get('order_id')

    if not order_id:
        return redirect('home')
    
    order = get_object_or_404(models.Order, id=order_id)
    payment_data = generate_sslcommerz_payment(request, order)
    

    if payment_data['status'] == 'SUCCESS':
        return redirect(payment_data['GatewayPageURL'])

    else:
        messages.error(request, 'Payment gateway error. Please Try again.')
        return redirect('checkout')







# 1. Payment Success
@csrf_exempt
@login_required
def payment_success(request, order_id):
    order = get_object_or_404(models.Order, id = order_id, user=request.user)


    order.paid = True                                           # order --> paid
    order.status = 'processing'                                 # order status --> processing
    order.transaction_id = order.id                             # take transaction id
    order.save()


    # get all the order items
    order_items = order.order_items.all()


    # for each item:
    for item in order_items:
        product = item.product                                  # get the exact one product each time
        product.stock -= item.quantity                          # product stock --> decrease



        if product.stock < 0:
            product.stock = 0                                    # if negative value comes by any issue, make stock 0
    
        product.save()



    # Send Confirmation email
    send_order_confirmation_email(order)

    messages.success(request, 'Payment Successful')

    return render(request, 'shop/payment_success.html', {'order' : order})







# 2. Payment Failed
@csrf_exempt
@login_required
def payment_fail(request, order_id):
    order = get_object_or_404(models.Order, id = order_id, user=request.user)

    order.status = 'canceled'

    order.save()
    return redirect('checkout')





# 3. Payment Cancel
@csrf_exempt
@login_required
def payment_cancel(request, order_id):
    order = get_object_or_404(models.Order, id = order_id, user=request.user)

    order.status = 'canceled'

    order.save()
    return redirect('cart_detail')








# profile view
@login_required
def profile_view(request):
    tab = request.GET.get('tab')                                                     # which tab is active               
    orders = models.Order.objects.filter(user = request.user)
    completed_orders = orders.filter(status = 'delivered')

    total_spent = sum(order.get_total_cost() for order in orders)
    order_history_active = (tab == 'orders')                                          # true if 'orders' tab is active, else false    

    for order in orders:
        print(order.id, "status:", order.status, "display:", order.get_status_display())



    context = {
        'user' : request.user,
        'orders' : orders,
        'completed_orders' : completed_orders,
        'total_spent' : total_spent,
        'order_history_active' : order_history_active
    }
   

    return render(request, 'shop/profile.html', context)    