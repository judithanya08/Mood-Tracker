from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_mood, name='add_mood'),
    path('history/', views.view_history, name='view_history'),
    path('edit/<int:entry_id>/', views.edit_mood, name='edit_mood'),
    path('delete/<int:entry_id>/', views.delete_mood, name='delete_mood'),
    path('trends/', views.mood_trends, name='mood_trends'),
    path('calendar/', views.mood_calendar, name='mood_calendar'),
]

