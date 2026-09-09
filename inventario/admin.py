from django.contrib import admin

from django.contrib import admin
from .models import MateriaPrima, ProductoTerminado, SalidaProducto, MaterialEnvaseEmpaque

# Registra tus modelos aquí.

# 1. Materia Prima
@admin.register(MateriaPrima)
class MateriaPrimaAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista principal del Admin
    list_display = ('nombre', 'cantidad', 'proveedor', 'fecha_vencimiento','lote','fecha_solicitud','fecha_envio')
    # Campos por los que se puede buscar
    search_fields = ('nombre', 'proveedor','lote')
    # Filtros laterales
    list_filter = ('fecha_vencimiento','fecha_solicitud', 'fecha_envio')

# 2. Producto Terminado
@admin.register(ProductoTerminado)
class ProductoTerminadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'estado')
    search_fields = ('nombre', 'codigo')
    list_filter = ('estado',)

# 3. Salida de Producto (Para ver los movimientos de inventario)
@admin.register(SalidaProducto)
class SalidaProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'fecha_salida')
    # Permite buscar por el nombre del producto relacionado
    search_fields = ('producto__nombre',)
    list_filter = ('fecha_salida',)
    
# 4. Material de Envase y Empaque
@admin.register(MaterialEnvaseEmpaque)
class MaterialEnvaseEmpaqueAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad')
    search_fields = ('nombre',)
# Register your models here.
