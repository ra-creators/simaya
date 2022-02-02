from django.urls import path
from . import views

urlpatterns = [
    path('rp_callback/', views.rp_callback, name='rp_callback'),
]
