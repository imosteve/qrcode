from django.urls import path
from . import views

urlpatterns = [
    # path('generate_qr/', views.generate_qr, name='generate_qr'),
    path('', views.generate_qr, name='generate_qr'),
]
