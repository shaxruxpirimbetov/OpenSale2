from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import permissions
from django.shortcuts import render
from .models import Product, ProductImages
from .serializers import ProductSerializer
from stores.models import Store
from stores.serializers import StoreSerializer
from user.models import SavedProduct
from user.serializers import SavedProductSerializer
from .funcs import search


class ProductApi(APIView):
	permission_classes = [permissions.AllowAny, permissions.IsAuthenticated]
	parser_classes = [MultiPartParser, FormParser, JSONParser]
	def get_permissions(self):
		if self.request.method == "GET":
			if self.request.GET.get("my"):
				return [permissions.IsAuthenticated()]
			return [permissions.AllowAny()]
		return [permissions.IsAuthenticated()]
		
	def get(self, request):
		product_id = request.GET.get("product_id")
		store_id = request.GET.get("store_id")
		my = request.GET.get("my")
		query = request.GET.get("q")
		if product_id:
			product = Product.objects.filter(id=product_id).first()
			if not product:
				return Response({"status": False, "message": "Product not found"})
			store = Store.objects.filter(id=product.store.id).first()
			store = StoreSerializer(store).data
			product = ProductSerializer(product).data
			product["store"] = store
			print("\n"*5, request.user, "\n"*5)
			if request.user.id:
				saved_product = SavedProduct.objects.filter(user=request.user, product_id=product.get("id")).first()
				product["saved"] = True if saved_product else False
			else:
				product["saved"] = "unauthorized"
			return Response({"status": True, "message": product})
		
		elif my:
			store = Store.objects.filter(user=request.user).first()
			if not store:
				return Response({"status": False, "message": "Store not found"})
			products = Product.objects.filter(store=store).all()
			products = ProductSerializer(products, many=True).data
			return Response({"status": True, "message": products})
		
		elif query:
			products = Product.objects.all()
			products = ProductSerializer(products, many=True).data
			results = search(query, products)
			return Response({"status": True, "message": results})
		
		elif store_id:
			store = Store.objects.filter(id=store_id).first()
			if not store:
				return Response({"status": False, "message": "Store not found"})
			products = Product.objects.filter(store=store).all()
			products = ProductSerializer(products, many=True).data
			return Response({"status": True, "message": products})
			
		products = Product.objects.all()
		products = ProductSerializer(products, many=True).data
		if request.user.id:
			for product in products:
				saved_product = SavedProduct(product_id=product.get("id")).first()
				product["saved"] = True if saved_product else False
		return Response({"status": True, "message": products})
	
	def post(self, request):
		title = request.data.get("title")
		description = request.data.get("description")
		price = request.data.get("price")
		images = request.FILES.getlist("images")
		
		if not all([title, description, price, images]):
			return Response({"status": False, "message": "store_id, title, description, price and images are required"})
		
		store = Store.objects.filter(user=request.user).first()
		if not store:
			return Response({"status": False, "message": "Store not found"})
		
		product = Product.objects.create(
		    store=store,
		    title=title,
		    description=description,
		    price=price
		)
		for image in images:
			ProductImages.objects.create(product=product, image=image)
		
		product = ProductSerializer(product).data
		return Response({"status": True, "message": product})
	
	def put(self, request):
		product_id = request.data.get("product_id")
		title = request.data.get("title")
		description = request.data.get("description")
		price = request.data.get("price")
		
		if not all([title, description, price]):
			return Response({"status": False, "message": "title, description and price are required"})
		
		store = Store.objects.filter(user=request.user).first()
		if not store:
			return Response({"status": False, "message": "Store not found"})
		
		product = Product.objects.filter(id=product_id, store=store).first()
		if not product:
			return Response({"status": False, "message": "Product not found"})
		
		product.title = title
		product.description = description
		product.price = price
		product.save()
		product = ProductSerializer(product).data
		return Response({"status": True, "message": product})
	
		

		
