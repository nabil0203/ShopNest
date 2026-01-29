from django.contrib import admin

from . import models

# Register your models here.


# category model
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):                                      # Model Admin used to customize
    list_display = ['name', 'slug']                                         # list_display
    prepopulated_fields = {'slug' : ('name',)}


# product model
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created_at', 'category']
    prepopulated_fields = {'slug' : ('name', )}


admin.site.register(models.Rating)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)



