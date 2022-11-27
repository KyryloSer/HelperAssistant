from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('add_note/', views.note, name='note'),
    path('add_tag/', views.tag, name='usertag'),
    path('detail/<int:note_id>', views.detail, name='detail'),
    path('done/<int:note_id>', views.set_done, name='set_done'),
    path('delete/<int:note_id>', views.delete_note, name='delete_note'),
    path('find_notes/', views.find_note, name='find_note'),
    path('show_notes/', views.show_notes, name='show_notes'),
    path('show_notes/<str:filter>', views.find_note, name='filter_note'),
    path('edit_note/<int:note_id>', views.edit_note, name='edit_note'),
]
