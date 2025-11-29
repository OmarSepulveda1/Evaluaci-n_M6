from django.urls import path
from . import views

urlpatterns = [
    # Tareas (Requieren autenticación)
    path('', views.tareas_list, name='tareas_list'),
    path('add/', views.tarea_add, name='tarea_add'),
    path('detail/<int:pk>/', views.tarea_detail, name='tarea_detail'),
    path('delete/<int:pk>/', views.tarea_delete, name='tarea_delete'),
    
    # Autenticación (Vistas personalizadas, no las de auth.urls)
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]