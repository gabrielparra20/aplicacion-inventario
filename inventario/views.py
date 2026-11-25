from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import MateriaPrimaForm, ProductoTerminadoForm, SalidaProductoForm, MaterialEnvaseEmpaqueForm
from datetime import date
from .models import MateriaPrima, ProductoTerminado, SalidaProducto, MaterialEnvaseEmpaque 
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm # Importamos el formulario de login de Django
from django.contrib.auth.decorators import login_required # Para proteger vistas
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm



def registro_view(request):
    """Maneja el registro de un nuevo usuario."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente tras registrarse
            messages.success(request, f"¡Cuenta creada! Bienvenido, {user.username}.")
            return redirect('dashboard')
        else:
            messages.error(request, "Por favor, corrige los errores del formulario.")
    else:
        form = UserCreationForm()

    return render(request, 'inventario/registrar_usuario.html', {'form': form})


def login_view(request):
    """Maneja la lógica de inicio de sesión."""
    # Si el usuario ya está autenticado, lo redirigimos al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido, {username}!")
                # Redirige a la URL configurada en settings.py o a 'dashboard'
                return redirect('dashboard') 
            else:
                messages.error(request, "Usuario o contraseña inválidos.")
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'inventario/login.html', {'form': form})

def logout_view(request):
    """Cierra la sesión del usuario."""
    logout(request)
    messages.info(request, "Sesión cerrada exitosamente.")
    return redirect('login') # Redirige a la página de login

@login_required
def dashboard(request):
    # --- Lógica para Materias Primas --
    
    total_materias_primas = MateriaPrima.objects.count()
    registros_materias_primas = MateriaPrima.objects.all().order_by('-id')[:10] 

    # Asumiendo los estados de MateriaPrima son 'Pendiente', 'Aprobado', 'En Análisis'/'Rechazado'
    materias_primas_pendientes = MateriaPrima.objects.filter(estado='Pendiente').count()
    materias_primas_aprobadas = MateriaPrima.objects.filter(estado='Aprobado').count()
    # Usaremos 'En Análisis' para el tercer conteo que la plantilla llama 'Terminadas'
    materias_primas_en_analisis = MateriaPrima.objects.filter(estado='En Análisis').count() 

    # --- Lógica para Productos Terminados ---
    productos_terminados = ProductoTerminado.objects.all()
    total_productos_terminados = productos_terminados.count()
    
    # Calcular el stock total y productos sin stock
    stock_total = productos_terminados.aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    productos_terminados_sin_stock = productos_terminados.filter(cantidad__lte=0).count()
    
    # --- Lógica para Material de Envase y Empaque ---
    total_material_envase = MaterialEnvaseEmpaque.objects.count()

    context = {
        # Para Materias Primas
        'total_materias_primas': total_materias_primas,
        'materias_primas_pendientes': materias_primas_pendientes,
        'materias_primas_aprobadas': materias_primas_aprobadas,
        'materias_primas_terminadas': materias_primas_en_analisis, # Usamos En Análisis para el conteo de 'Terminadas'
        'materias_primas': registros_materias_primas,
        'total_material_envase': total_material_envase,
        # Para Productos Terminados
        'productos_terminados': productos_terminados,
        'total_productos_terminados': total_productos_terminados,
        'stock_total': stock_total,
        'productos_terminados_sin_stock': productos_terminados_sin_stock,
        
        # Para Material de Envase
        'total_material_envase': total_material_envase,
    }
    
    # CORRECCIÓN: Ahora la función pasa el contexto completo
    return render(request, 'inventario/dashboard.html', context)

# def listar_materia_prima(request):
#     # CORRECCIÓN: Se agrega la vista faltante para listar materia prima
#     materias_primas = MateriaPrima.objects.all()
#     context = {
#         'titulo': 'Listado de Materias Primas',
#         'materias_primas': materias_primas,
#     }
#     return render(request, 'inventario/listar_materia_prima.html', context)



# from .models import MateriaPrima # Asegúrate de importar el modelo MateriaPrima
# from .forms import MateriaPrimaForm # Asegúrate de importar el formulario
@login_required
def registrar_materia_prima(request):
    if request.method == 'POST':
        # 1. Crea el formulario con los datos POST
        form = MateriaPrimaForm(request.POST)
        
        # 2. Verifica si el formulario es válido
        if form.is_valid():
            nueva_materia_prima = form.save(commit=False)
            
            # ⭐️ MODIFICACIÓN CLAVE: Lógica robusta para generar el código único ⭐️
            try:
                # Inicializa el contador basado en la cantidad actual (el punto de partida)
                consecutivo = MateriaPrima.objects.count() + 1
                
                # Bucle de reintento: Garantiza que el código no exista
                # Esto soluciona el problema de que el contador se base en un registro borrado
                while MateriaPrima.objects.filter(codigo=f"MP-{consecutivo:04d}").exists():
                    consecutivo += 1
                    
                # Genera el código final
                nuevo_codigo = f"MP-{consecutivo:04d}" 
                nueva_materia_prima.codigo = nuevo_codigo
                
            except Exception as e:
                # Este error es muy raro (por ejemplo, si falla la DB),
                # pero si ocurre, no redirijas, solo muestra el error en la misma página.
                messages.error(request, f"Error CRÍTICO al generar el código: {e}")
                # El código continuará a 'context' y renderizará la página
                
            # 3. Guarda el objeto en la base de datos
            nueva_materia_prima.save()
            messages.success(request, "Materia prima registrada exitosamente.")
            return redirect('dashboard')
            
        else:
            # 4. Manejo de error de validación
            # Si el formulario NO es válido, el mensaje de error se muestra.
            # NO agregamos 'return redirect', permitimos que la función siga y
            # que el template se renderice con los errores del formulario.
            messages.error(request, "Error en el formulario. Por favor, revisa los datos.")
            
    else:
        # Petición GET: Muestra el formulario vacío
        form = MateriaPrimaForm()
        
    context = {
        'form': form,
        'titulo': 'Registrar Materia Prima'
    }
    # 5. Renderiza el template (con el formulario lleno y los errores, si falló el POST)
    return render(request, 'inventario/registrar_materia_prima.html', context)

@login_required
def editar_materia_prima(request, pk):
    materia_prima = get_object_or_404(MateriaPrima, pk=pk)
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST, instance=materia_prima)
        if form.is_valid():
            form.save()
            messages.success(request, "Materia prima actualizada exitosamente.")
            return redirect('dashboard')
        else:
            messages.error(request, "Error al actualizar la materia prima.")
    else:
        form = MateriaPrimaForm(instance=materia_prima)
        
    context = {
        'form': form,
        'titulo': f'Editar Materia Prima: {materia_prima.nombre}'
    }
    return render(request, 'inventario/registrar_materia_prima.html', context) # Reutiliza la plantilla de registro

@login_required
def eliminar_materia_prima(request, pk):
    materia_prima = get_object_or_404(MateriaPrima, pk=pk)
    if request.method == 'POST':
        materia_prima.delete()
        messages.success(request, f"Materia prima '{materia_prima.nombre}' eliminada correctamente.")
        return redirect('dashboard')
        
    context = {
        'materia_prima': materia_prima,
    }
    return render(request, 'inventario/confirmar_eliminacion.html', context)


# --- Vistas para Producto Terminado ---
@login_required
def registrar_producto_terminado(request):
    if request.method == 'POST':
        form = ProductoTerminadoForm(request.POST)
        if form.is_valid():
            nuevo_producto = form.save(commit=False)
            
            # Generar el código de forma automática
            try:
                cantidad_registros = ProductoTerminado.objects.count()
                nuevo_codigo = f"PT-{cantidad_registros + 1:04d}" # Formato con 4 dígitos
                nuevo_producto.codigo = nuevo_codigo
            except Exception as e:
                messages.error(request, f"Error al generar el código: {e}")
                return redirect('registrar_producto_terminado')

            nuevo_producto.save()
            messages.success(request, "Producto terminado registrado exitosamente.")
            return redirect('dashboard')
        else:
            messages.error(request, "Error en el formulario. Por favor, revisa los datos.")
    else:
        form = ProductoTerminadoForm()
        
    context = {
        'form': form,
        'titulo': 'Registrar Producto Terminado'
    }
    return render(request, 'inventario/registrar_producto_terminado.html', context)

@login_required
def editar_producto_terminado(request, pk):
    producto = get_object_or_404(ProductoTerminado, pk=pk)
    if request.method == 'POST':
        form = ProductoTerminadoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto terminado actualizado exitosamente.")
            return redirect('dashboard')
        else:
            messages.error(request, "Error al actualizar el producto terminado.")
    else:
        form = ProductoTerminadoForm(instance=producto)
        
    context = {
        'form': form,
        'titulo': f'Editar Producto Terminado: {producto.nombre}'
    }
    return render(request, 'inventario/registrar_producto_terminado.html', context) # Reutiliza la plantilla de registro

@login_required
def eliminar_producto_terminado(request, pk):
    producto = get_object_or_404(ProductoTerminado, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, f"Producto terminado '{producto.nombre}' eliminado correctamente.")
        return redirect('dashboard')
        
    context = {
        'producto': producto,
    }
    return render(request, 'inventario/producto_terminado_confirm_delete.html', context)
    
# --- Vistas de Proceso y Salida ---

@login_required
def salida_producto(request):
    form = SalidaProductoForm()
    
    if request.method == 'POST':
        form = SalidaProductoForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad_salida = form.cleaned_data['cantidad']
            
            if producto.cantidad >= cantidad_salida:
                producto.cantidad -= cantidad_salida
                producto.save()
                SalidaProducto.objects.create(
                    producto=producto, 
                    cantidad=cantidad_salida
                )
                messages.success(request, "Salida de producto registrada exitosamente.")
                return redirect('dashboard')
            else:
                messages.error(request, "Error: No hay suficiente stock para esta salida.")

    productos = ProductoTerminado.objects.all()
    context = {
        'form': form,
        'title': 'Registro de Salida de Producto',
        'productos': productos,
    }
    return render(request, 'inventario/salida_producto.html', context)

@login_required
def registrar_material_envase(request):
    form = MaterialEnvaseEmpaqueForm()
    
    if request.method == 'POST':
        form = MaterialEnvaseEmpaqueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Material de envase y empaque registrado exitosamente.")
            return redirect('dashboard')
    
    context = {
        'form': form,
        'title': 'Registro de Material de Envase y Empaque'
    }
    return render(request, 'inventario/registrar_material_envase.html', context)

@login_required
def editar_material_envase(request, pk):
    """Permite editar un registro de Material de Envase y Empaque existente."""
    # Obtiene el objeto, o devuelve un 404 si no existe
    material = get_object_or_404(MaterialEnvaseEmpaque, pk=pk)
    
    if request.method == 'POST':
        # Instancia el formulario con los datos POST y la instancia del material
        form = MaterialEnvaseEmpaqueForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, f"El material '{material.nombre}' ha sido actualizado exitosamente.")
            # Redirige a la lista de materiales
            return redirect('listar_material_envase')
    else:
        # GET: Muestra el formulario con los datos actuales del material
        form = MaterialEnvaseEmpaqueForm(instance=material)
        
    context = {
        'form': form,
        'material': material,
        'title': 'Editar Material de Envase y Empaque',
    }
    return render(request, 'inventario/editar_material_envase.html', context)

@login_required
def eliminar_material_envase(request, pk):
    """Permite eliminar un registro de Material de Envase y Empaque."""
    material = get_object_or_404(MaterialEnvaseEmpaque, pk=pk)
    
    if request.method == 'POST':
        # Si se confirma la eliminación (POST)
        material.delete()
        messages.success(request, f"El material '{material.nombre}' ha sido eliminado correctamente.")
        # Redirige a la lista de materiales
        return redirect('listar_material_envase')
        
    context = {
        'objeto': material, # Usamos 'objeto' para que el template de confirmación sea reutilizable
        'nombre_modulo': 'Material de Envase y Empaque',
        'nombre_item': material.nombre
    }
    # Usaremos un template de confirmación de eliminación genérico
    return render(request, 'inventario/confirmar_eliminacion_generico.html', context)

@login_required
def listar_material_envase(request):
    """Muestra una lista de todos los materiales de envase y empaque registrados."""
    materiales = MaterialEnvaseEmpaque.objects.all().order_by('nombre')
    
    context = {
        'titulo': 'Inventario de Materiales de Envase y Empaque',
        'materiales': materiales,
    }
    return render(request, 'inventario/listar_material_envase.html', context)

@login_required
def productos_pendientes(request):
    # Filtra los productos que NO están en estado 'Aprobado' o 'Rechazado' (asumiendo que están listos para análisis)
    productos_pendientes = ProductoTerminado.objects.exclude(estado__in=['Aprobado', 'Rechazado'])

    context = {
        'productos_pendientes': productos_pendientes,
    }
    return render(request, 'inventario/productos_pendientes.html', context)
@login_required  
def liberar_producto(request, pk):
    producto = get_object_or_404(ProductoTerminado, pk=pk)
    
    if request.method == 'POST':
        # Lógica para liberar (cambiar estado a 'Aprobado')
        producto.estado = 'Aprobado'
        producto.save()
        messages.success(request, f"Producto terminado '{producto.nombre}' liberado y listo para salida.")
        return redirect('productos_pendientes')

    return render(request, 'inventario/liberar_producto.html', {'producto': producto})



