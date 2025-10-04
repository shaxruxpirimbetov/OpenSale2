from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Store
		fields = "__all__"


'''
class ProductImagesSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImages
		fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
	images = ProductImagesSerializer(many=True, source="productimages_set")
	class Meta:
		model = Product
		fields = "__all__"
'''	