
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tareas.urls')),
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
]