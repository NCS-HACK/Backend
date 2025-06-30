from django.urls import path
from . import views  # or use: from yourapp import views

urlpatterns = [
    path('users/', views.user_list, name='user-list'),
    path('users/<int:user_id>/', views.get_user, name='get_user'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/update/', views.update_user, name='update_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:task_id>/', views.get_task, name='get_task'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('events/', views.list_events, name='event-list'),
    path('events/create/', views.create_event, name='event-create'),
    path('events/<int:event_id>/', views.get_event, name='event-detail'),
    path('events/<int:event_id>/update/', views.update_event, name='event-update'),
    path('events/<int:event_id>/delete/', views.delete_event, name='event-delete'),
]
