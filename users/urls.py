from django.urls import path, include

from users import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.login_view, name='login'),
]
