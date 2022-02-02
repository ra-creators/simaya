from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('',views.blog_page,name="blog"),
    path('blogdetail/<int:pk>',views.blog_detail,name="blogdetail")
 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
