from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import permissions
from django.shortcuts import render
from .serializers import UserSerializer, SavedProductSerializer
from .models import SavedProduct
from products.models import Product
from stores.models import Store
from stores.serializers import StoreSerializer


class RegisterApi(APIView):
	permission_classes = [permissions.AllowAny]
	parser_classes = [MultiPartParser, FormParser, JSONParser]
	def post(self, request):
		username = request.data.get("username")
		password = request.data.get("password")
		
		if not all([username, password]):
			return Response({"status": False, "message": "username and password are required"})
		
		if len(username) < 3 or len(password) < 5:
			return Response({"status": False, "message": "username or password so verify"})
		
		user = User.objects.filter(username=username).first()
		if user:
			return Response({"status": False, "message": "username already exists"})
		
		user = User.objects.create_user(username=username, password=password)
		user = UserSerializer(user).data
		return Response({"status": True, "message": user})
	
	def put(self, request):
		username = request.data.get("username")
		if not username:
			return Response({"status": False, "message": "username are required"})
		
		user = User.objects.filter(username=username).first()
		if user:
			return Response({"status": False, "message": "User already exists"})
		
		request.user.username = username
		request.user.save()
		user = UserSerializer(request.user).data
		return Response({"status": True, "message": user})


class SavedProductApi(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		my = reuqest.data.get("my")
		if my:
			saved_products = SavedProduct.objects.filter(user=request.user).all()
			saved_products = SavedProductSerializer(saved_products, many=True).data
			return Response({"status": True, "message": saved_products})
			
		saved_products = SavedProduct.objects.all()
		saved_products = SavedProductSerializer(saved_products, many=True).data
		return Response({"status": True, "message": saved_products})
	
	def post(self, request):
		product_id = request.data.get("product_id")
		if not product_id:
			return Response({"status": False, "message": "product_id are required"})
		
		product = Product.objects.filter(id=product_id).first()
		if not product:
			return Response({"status": False, "message": "Product not found"})
		
		saved_product = SavedProduct.objects.filter(user=request.user, product=product).first()
		if saved_product:
			saved_product.delete()
			return Response ({"status": True, "message": "saved_product deleted successfully", "type": "deleted"})
		else:
			saved_product = SavedProduct.objects.create(user=request.user, product=product)
			saved_product = SavedProductSerializer(saved_product).data
			return Response({"status": True, "message": saved_product, "type": "added"})


class GetMeApi(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		user = UserSerializer(request.user).data
		store = Store.objects.filter(user=request.user).first()
		user["is_seller"] = True if store else False
		if user["is_seller"]:
			store = StoreSerializer(store).data
			user["store"] = store
		return Response({"status": True, "message": user})


