from django.contrib.auth.models import User
from django.db import models


class Store(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=24)
	description = models.TextField()
	logo = models.ImageField(upload_to="store_logos/")
	storename = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"Store {self.title}"
	
	class Meta:
		verbose_name = "Store"
		verbose_name_plural = "Stores"
