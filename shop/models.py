from django.db import models

from django.contrib.auth.models import User                                         # rating model

from django.core.validators import MinValueValidator, MaxValueValidator             # rating model

# Create your models here.






# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)                        # slug used for URL; unique = true--> 1 name for 1 product
    description = models.TextField()


    class Meta:
        verbose_name_plural = "Categories" 

    def __str__(self):
        return self.name
    





# Product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    
    price = models.DecimalField(max_digits=10, decimal_places=2)                            # 405.99
    stock = models.PositiveBigIntegerField(default=1)                                       # 1 product minimum
    available = models.BooleanField(default=True)                                           # if the product is available or not; By default Available, can make is unavailable 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to='products/%Y/%m/%d')                                 # images will be uploaded to the product folder based on date



    def __str__(self):
        return self.name
    

    # Rating for each product
    # 1 product has been purchased by 10 people
    # 5 people gave rating --> 4.5, 5, 3, 4, 2.5
    # We will show the Mean score of the rating for each product using a Function
    def average_rating(self):
        ratings = self.rating.all()                                                            # 'self.rating.all()'--> here 'rating' is the "related_name='ratings'" of Rating model

        if ratings.count > 0:
            return sum([i.rating for i in ratings])/ratings.count()








# Rating model

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])                      # rating range (1-5)                  
    
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}"









# Cart Model
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Total Price of the cart
    # Bazarer bag ee je koyta product ache, tar full price
    # 10 pants + 4 shirts + 5 shoes = 3560 total
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())                            # 'get_cost()' & 'items'(related_name='items) is from CartItem Model
                                                                                            # get_cost() ---> full price of each product
                                                                                            # items ---> how many items are there

     # total number of items
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all()) 








# Cart Item
# Every Cart can have multiple different items
# Every Cart can have multiple same items
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} X {self.product.name}"                          # Output as: 4 X Shirt


    # Total Price of the cart items
    # Bazarer bag ee je product ache, tader alada alada full price
    # 10 pants = 540, 4 shirts = 400, 5 shoes = 800
    def get_cost(self):
        return self.quantity*self.product.price                             # each item quantity * it's price










# Oder Model
class Order(models.Model):


    # choice list
    STATUS = [
        ('pending', 'Pending'),                                 # 1st value = backend
        ('processing', 'Processing'),                           # 2nd value = Fronted
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    postal_code = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    city = models.CharField(max_length=100)
    note = models.TextField()
    paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10, choices=STATUS)


    def __str__(self):
        return f"Order #{self.id}"                       # Order #2


    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())                  # 'get_cost()' from CartItem model
                                                                                        # "self.order_items.all()"-----> 'order_items' from OrderItem Model








# Order Item model

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_cost(self):
        return self.quantity*self.product.price  # 20
        

    