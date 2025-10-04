from django.contrib.auth.models import User
from django.db import models


class Version(models.Model):
	version = models.CharField(max_length=24)
	description = models.TextField()
	update_url = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"Version {self.version}"
	
	class Meta:
		verbose_name = "Version"
		verbose_name_plural = "Versions"

