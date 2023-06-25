from django.urls import path, include
from . views import book

urlpatterns = [
    path("", book, name="book")
]