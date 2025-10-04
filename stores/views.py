from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import permissions
from django.shortcuts import render
from .models import Store
from .serializers import StoreSerializer



class StoreApi(APIView):
	permission_classes = [permissions.AllowAny, permissions.IsAuthenticated]
	parser_classes = [MultiPartParser, FormParser, JSONParser]
	def get_permissions(self):
		if self.request.method == "GET":
			if self.request.GET.get("my"):
				return [permissions.IsAuthenticated()]
			return [permissions.AllowAny()]
		else:
			return [permissions.IsAuthenticated()]

	def get(self, request):
		my = request.GET.get("my")
		if my:
			store = Store.objects.filter(user=request.user).first()
			store = StoreSerializer(store).data
			return Response({"status": True, "message": store})
			
		stores = Store.objects.all()
		stores = StoreSerializer(stores, many=True).data
		return Response({"status": True, "message": stores})
	
	def post(self, request):
		title = request.data.get("title")
		description = request.data.get("description")
		logo = request.FILES.get("logo")
		
		print(request.data)
		
		if not all([title, description, logo]):
			return Response({"status": False, "message": "title, description and logo are required"})
		
		store = Store.objects.filter(storename=title.replace(" ", "").lower()).first()
		my_store = Store.objects.filter(user=request.user).first()
		if store or my_store:
			return Response({"status": False, "message": f"Store with name {title} already exists, or do you already have a store?"})
		
		store = Store.objects.create(
		    user=request.user,
		    title=title,
		    description=description,
		    logo=logo,
		    storename=title.replace(" ", "").lower()
		)
		store = StoreSerializer(store).data
		return Response({"status": True, "message": store})
	
	def put(self, request):
		title = request.data.get("title")
		description = request.data.get("description")
		
		if not all([title, description]):
			return Response({"status": False, "message": "title and description are required"})
		
		store = Store.objects.filter(user=request.user).first()
		if not store:
			return Response({"status": False, "message": "Store not found"})
		
		store.title = title
		store.description = description
		store.storename = title.replace(" ", "").lower()
		store.save()
		store = StoreSerializer(store).data
		return Response({"status": True, "message": store})



