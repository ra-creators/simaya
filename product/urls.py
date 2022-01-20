from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # product
    path('categories/', views.categories, name='categories'),
    path('categories/<slug:cat_slug>/', views.categories, name='list_by_category'),
]
