from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('search/', views.search, name="search"),
    path('detail/', views.detail, name="detial"),
]

