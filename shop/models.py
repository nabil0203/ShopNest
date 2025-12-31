from django.db import models

# Create your models here.


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)                        # unique = true; 1 name for 1 product
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

    image = models.ImageField(upload_to='products/%Y/%m/%d')                                 # upload_to
    



