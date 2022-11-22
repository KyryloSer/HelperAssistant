from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start, name='start'),
    path('add_note/', views.note, name='note'),
    path('add_tag/', views.tag, name='usertag'),
    path('detail/<int:note_id>', views.detail, name='detail'),
    path('done/<int:note_id>', views.set_done, name='set_done'),
    path('delete/<int:note_id>', views.delete_note, name='delete_note'),
    path('find_notes/', views.find_note_rend, name='find_note_rend'),
    # path('find_notes/<str:q>', views.find_note, name='find_note'),
    path('find_notes/<str:q>/', views.find_note, name='find_note')
]
