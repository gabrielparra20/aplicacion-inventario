from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 

# Opciones de Estatus y Unidades
ESTADO_CHOICES = (
    ('Pendiente', 'Pendiente'),
    ('En Análisis', 'En Análisis'),
    ('Aprobado', 'Aprobado'),
    ('Rechazado', 'Rechazado'),
)

UNIDAD_CHOICES = (
    ('kg', 'Kilogramos'),
    ('L', 'Litros'),
    ('u', 'Unidades'),
    ('g', 'Gramos'),
    ('mL', 'Mililitros'),
)

# --- MODELOS ---

class MateriaPrima(models.Model):
    # La definición de MateriaPrima se mantiene igual a como la enviaste
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    proveedor = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=20, choices=UNIDAD_CHOICES, default='u')
    lote = models.CharField(max_length=100, blank=True, null=True)
    fecha_solicitud = models.DateField(blank=True,null=True)
    fecha_envio = models.DateField(blank=True, null= True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    
    class Meta:
        verbose_name = "Materia Prima"
        verbose_name_plural = "Materias Primas"

    def __str__(self):
        return self.nombre

class ProductoTerminado(models.Model):
    # ¡CAMPOS CORREGIDOS Y AÑADIDOS! Ahora son 8 campos, como tu formulario esperaba
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True) # Campo añadido
    nombre = models.CharField(max_length=100)
    proveedor = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    lote = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidad_medida = models.CharField(max_length=20, choices=UNIDAD_CHOICES, default='u') # Campo añadido
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente') # Campo añadido
    fecha_solicitud = models.DateTimeField(blank=True, null=True) 
    fecha_envio = models.DateField(blank=True,null=True)



    
    def __str__(self):
        return self.nombre

class SalidaProducto(models.Model):
    # 'producto' hace referencia al ProductoTerminado del cual sale stock
    producto = models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE) 
    cantidad = models.IntegerField()
    fecha_salida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Salida de Producto"
        verbose_name_plural = "Salidas de Productos"

    def __str__(self):
        # CORRECCIÓN: Ahora retorna el nombre del producto relacionado.
        return f"Salida de {self.cantidad} de {self.producto.nombre}"

class MaterialEnvaseEmpaque(models.Model):
    # Se añade la unidad de medida
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    unidad_medida = models.CharField(max_length=20, choices=UNIDAD_CHOICES, default='u') # Campo añadido
    proveedor = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    lote = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    fecha_solicitud = models.DateField(blank=True, null=True) 
    fecha_envio = models.DateField(blank=True,null=True)
    def __str__(self):
        return self.nombre
