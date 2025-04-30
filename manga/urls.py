from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/add/', views.progress_add, name='progress_add'),
    path('project/<int:pk>/today/', views.progress_today, name='progress_today'),
    path('project/<int:pk>/today/confirm/', views.progress_today_confirm, name='progress_today_confirm'),
    path('project/<int:pk>/today/save/', views.progress_today_save, name='progress_today_save'),
    path('progress/<int:progress_id>/delete/', views.progress_delete, name='progress_delete'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
]

