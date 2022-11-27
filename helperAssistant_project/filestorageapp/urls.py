from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('upload/', views.upload, name='upload'),
    path('picture/<str:pk>', views.viewPicture, name='picture'),
    path('delete_picture/<str:pk>', views.delete_picture, name='delete_picture'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
