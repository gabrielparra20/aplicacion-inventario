from django.urls import path ,include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    #login iniciar sesion 
    path('accounts/login/', views.login_view, name='login'), # Usaremos esta vista custom
    path('logout/', views.logout_view, name='logout'),
    
    # Rutas para MateriaPrima
    path('materia_prima/registrar/', views.registrar_materia_prima, name='registrar_materia_prima'),
    # **NUEVA RUTA para listar Materia Prima**
   
    path('materia_prima/editar/<int:pk>/', views.editar_materia_prima, name='editar_materia_prima'),
    path('materia_prima/eliminar/<int:pk>/', views.eliminar_materia_prima, name='eliminar_materia_prima'),
    
    # Rutas para ProductoTerminado
    path('producto_terminado/registrar/', views.registrar_producto_terminado, name='registrar_producto_terminado'),
    path('producto_terminado/editar/<int:pk>/', views.editar_producto_terminado, name='producto_terminado_edit'),
    path('producto_terminado/eliminar/<int:pk>/', views.eliminar_producto_terminado, name='producto_terminado_confirm_delete'),
    
    # Rutas para Salida y Material
    path('salida_producto/', views.salida_producto, name='salida_producto'),
    path('material_envase/registrar/', views.registrar_material_envase, name='registrar_material_envase'),
    path('material_envase/listado/', views.listar_material_envase, name='listar_material_envase'),
    path('material_envase/editar/<int:pk>/', views.editar_material_envase, name='editar_material_envase'),
    path('material_envase/eliminar/<int:pk>/', views.eliminar_material_envase, name='eliminar_material_envase'),
    # Rutas para Liberación
    path('productos_pendientes/', views.productos_pendientes, name='productos_pendientes'),
    path('productos_pendientes/liberar/<int:pk>/', views.liberar_producto, name='liberar_producto'),
]
