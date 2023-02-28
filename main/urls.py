from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('brands/', views.brands, name='brands'),
    path('brands/<int:brand_id>', views.brand, name='brand'),
    path('products/', views.products, name='products'),
    path('products/<int:pk>', views.ProductDetailView.as_view(),name='product-detail'),
    path('product-reviews', views.ReviewListApi.as_view()),
    path('product-review/<int:product_id>',views.add_review, name='review'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('favorites/', views.favorites, name='favorites'),
    path('product/<int:product_id>/add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('product_detail/<int:product_id>', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
]



