from django.contrib.auth.models import User
from django.db import models
from products.models import Product


class SavedProduct(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"Saved Product {self.title}"
	
	class Meta:
		verbose_name = "Saved Product"
		verbose_name_plural = "Saved Products"

