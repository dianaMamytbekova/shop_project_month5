from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg, Count


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)  
    rating = serializers.FloatField(read_only=True)  

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)  

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']
