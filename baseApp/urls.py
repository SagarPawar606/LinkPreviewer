from django.urls import path
from .views import preview

urlpatterns = [
    path('', preview, name='index'),
]