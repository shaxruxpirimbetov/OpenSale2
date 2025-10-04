from django.urls import path
from . import views

urlpatterns = [
    path("", views.StoreApi.as_view()),
    
]