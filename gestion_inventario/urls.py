"""
URL configuration for gestion_inventario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# gestion_inventario/urls.py
from django.contrib import admin
from django.urls import path, include
from inventario import views  # Importa las vistas de tu aplicación de inventario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'), # Agrega esta línea para la página de inicio
    path('', include('inventario.urls'))
]

