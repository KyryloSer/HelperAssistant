from django.urls import path
from . import views

urlpatterns = [
    path('files/', views.view_files, name='view_files'),
    path('files/filter/<str:filters>', views.filter_files, name='filter_files'),
    path('files/add/', views.file_upload, name='file_upload'),
    path('files/down/<int:file_id>', views.file_download, name='file_download'),
]