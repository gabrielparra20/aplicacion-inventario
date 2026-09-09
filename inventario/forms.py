from django import forms
from .models import MateriaPrima, ProductoTerminado, SalidaProducto, MaterialEnvaseEmpaque

# --- Formularios para Modelos ---

class MateriaPrimaForm(forms.ModelForm):
    """
    Formulario para registrar y editar Materias Primas.
    Asegura que solo los campos relevantes sean editables y que la unidad de medida
    use las opciones definidas en el modelo.
    """
    class Meta:
        model = MateriaPrima
        # Excluir 'codigo' para que se genere automáticamente en la vista.
        fields = ['nombre', 'proveedor', 'fabricante', 'cantidad', 'unidad_medida', 'fecha_vencimiento', 'estado', 'lote','fecha_solicitud','fecha_envio']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_solicitud': forms.DateInput(attrs={'type': 'date'}),
            'fecha_envio': forms.DateInput(attrs={'type': 'date'}),
        }

class ProductoTerminadoForm(forms.ModelForm):
    """
    Formulario para registrar y editar Productos Terminados.
    """
    class Meta:
        model = ProductoTerminado
        # Excluir 'codigo', 'estado' y 'fecha_creacion' para manejo automático.
        fields = ['nombre','proveedor', 'fabricante','lote', 'cantidad', 'unidad_medida','fecha_solicitud','fecha_envio','estado']
        widgets = {
            'fecha_solicitud': forms.DateInput(attrs={'type': 'date'}),
            'fecha_envio': forms.DateInput(attrs={'type': 'date'}),
           
        }

# ... (código existente)

class MaterialEnvaseEmpaqueForm(forms.ModelForm):
    """
    Formulario para registrar Material de Envase y Empaque.
    """
    class Meta:
        model = MaterialEnvaseEmpaque
        fields = ['nombre','proveedor', 'fabricante','lote','unidad_medida', 'cantidad','fecha_solicitud','fecha_envio','estado']
        widgets = {
            'fecha_solicitud': forms.DateInput(attrs={'type': 'date'}),
            'fecha_envio': forms.DateInput(attrs={'type': 'date'}),
           
        }
    # ⭐️ AGREGAR O MODIFICAR ESTE MÉTODO ⭐️
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Aplicar el empty_label para obligar al usuario a elegir una opción válida.
        # Si no lo eligen, fallará la validación.
        self.fields['unidad_medida'].empty_label = "--- Seleccione la Unidad de Medida ---"
        
        # 2. Aplicar clases Tailwind a todos los campos (opcional, pero buena práctica si no lo hiciste en el HTML)
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'mt-1 block w-full rounded-xl border-gray-300 shadow-sm focus:border-yellow-500 focus:ring-yellow-500 sm:text-sm p-3 border'
            })

# --- Formulario Específico para Salida de Producto ---

class SalidaProductoForm(forms.Form):
    """
    Formulario para manejar la salida de stock de Producto Terminado.
    Usa ModelChoiceField para seleccionar el producto disponible.
    """
    producto = forms.ModelChoiceField(
        queryset=ProductoTerminado.objects.filter(estado='Aprobado'), # Solo productos APROBADOS
        label="Producto a Despachar",
        empty_label="--- Seleccione un Producto ---",
    )
    cantidad = forms.IntegerField(
        label="Cantidad de Salida",
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Ingrese la cantidad'}),
    )
