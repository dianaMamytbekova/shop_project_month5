from rest_framework import generics
from django.db.models import Avg, Count
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductWithReviewsSerializer
)



class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategorySerializer



class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class ProductWithReviewsAPIView(generics.ListAPIView):
    serializer_class = ProductWithReviewsSerializer

    def get_queryset(self):
        return Product.objects.annotate(rating=Avg('reviews__stars')).prefetch_related('reviews')



class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
