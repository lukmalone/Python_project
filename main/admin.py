from django.contrib import admin
from .models import Category, Product, Order, Favorite, ProductReview, Profile


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'created_by', 'name')
    list_filter = ('in_stock', 'quantity')
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'date_created', 'reviewer', 'content')

admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Favorite)
admin.site.register(Profile)