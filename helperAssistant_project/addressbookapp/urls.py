
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='addressbookapp_main'),
    path('add_contact/', views.add_contact, name='add-contact'),
    path('delete_contact/<int:pk>/', views.delete_contact, name='delete-contact'),
    path('find-contacts/', views.find_contacts, name='find-contacts'),
    path('detail/<int:pk>/', views.ContactDetailView.as_view(), name='detail'),
    path('edit_contact/<int:pk>/', views.edit_contact, name='edit-contact'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('birthdays/', views.BirthdayView.as_view(), name='birthdays'),
    path('fake/', views.add_fake_contact, name = 'add_fake_contact'),
]