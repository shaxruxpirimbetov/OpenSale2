from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import permissions
from django.shortcuts import render
from .models import Version
from .serializers import VersionSerializer


class VersionApi(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		versions = Version.objects.all()
		versions = VersionSerializer(versions, many=True).data
		return Response({"status": True, "message": versions})
	
	def post(self, request):
		version = request.data.get("version")
		description = request.data.get("description")
		update_url = request.data.get("update_url")
		
		if not request.user.username == "shaxrux":
			return Response({"status": False, "message": "Permission error"})
		
		if not all([version, description, update_url]):
			return Response({"status": False, "message": "version and description are required"})
		
		version = Version.objects.filter(version=version).first()
		if version:
			return Response({"status": False, "message": "Version already exists"})
		
		version = Version.objects.create(version=version, description=description, update_url=update_url)
		version = VersionSerializer(version).data
		return Response({"status": True, "message": version})

