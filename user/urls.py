from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterApi.as_view()),
    path("saved_product/", views.SavedProductApi.as_view()),
    path("get_me/", views.GetMeApi.as_view()),
    
]