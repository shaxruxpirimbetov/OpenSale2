from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Version


class VersionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Version
		fields = "__all__"

