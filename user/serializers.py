from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SavedProduct

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = "__all__"


class SavedProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = SavedProduct
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