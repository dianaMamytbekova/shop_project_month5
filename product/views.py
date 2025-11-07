from rest_framework import generics
from django.db.models import Avg, Count
from .models import Category, Product, Review
from .serializers import (
    CategoryWithCountSerializer,
    ProductWithReviewsSerializer,
    ReviewSerializer,
    ProductSerializer
)

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategoryWithCountSerializer

class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategoryWithCountSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductWithReviewsAPIView(generics.ListAPIView):
    serializer_class = ProductWithReviewsSerializer

    def get_queryset(self):
        return Product.objects.annotate(rating=Avg('reviews__stars')).prefetch_related('reviews')

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
