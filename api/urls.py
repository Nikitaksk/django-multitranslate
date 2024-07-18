from django.urls import path
from . import views

urlpatterns = [
    path('translate/', views.textApiView.as_view(), name='translate'),
]
