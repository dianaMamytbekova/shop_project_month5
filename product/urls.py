from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:pk>/', views.CategoryDetailAPIView.as_view()),
    
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),

    path('products/reviews/', views.ProductWithReviewsAPIView.as_view()),

    path('reviews/', views.ReviewListAPIView.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetailAPIView.as_view()),
]
