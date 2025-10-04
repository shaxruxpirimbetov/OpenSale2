from django.urls import path
from . import views

urlpatterns = [
    path("", views.VersionApi.as_view()),
]