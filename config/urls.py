from django.urls import path
from . import views

urlpatterns = [
    path('', views.handle_uploaded_file, name='handle_uploaded_file'),
    path('', views.upload, name='upload'),
    path('', views.upload_complete, name='upload_complete'),
]
