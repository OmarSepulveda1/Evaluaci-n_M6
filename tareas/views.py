from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import TareaForm

# --- ESTRUCTURA DE DATOS EN MEMORIA (In-Memory Task Storage) ---
# Almacenamiento: { 'user_id_str': [{'id': 1, 'title': '...', 'description': '...', 'user_id': 1}, ...] }

IN_MEMORY_TASKS = {}
global_task_id_counter = 0

def get_next_task_id():
    """Genera un ID único global. Nota: Se reinicia al reiniciar el servidor."""
    global global_task_id_counter
    global_task_id_counter += 1
    return global_task_id_counter

def get_user_tasks(user_id):
    """Devuelve la lista de tareas del usuario o una lista vacía. Usa el ID como string."""
    
    return IN_MEMORY_TASKS.setdefault(str(user_id), [])

def get_task_by_id(user_id, task_id):
    """Busca y devuelve una tarea por ID para un usuario específico."""
    tasks = get_user_tasks(user_id)
    try:
       
        return next(t for t in tasks if t['id'] == task_id)
    except StopIteration:
        return None

# --- VISTAS DE AUTENTICACIÓN ---

def register(request):
    if request.user.is_authenticated:
        return redirect('tareas_list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. Bienvenido!')
            return redirect('tareas_list')
        else:
           
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'registro_de_usuario.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('tareas_list')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
           
            return redirect('tareas_list')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
        
    context = {'form': form}
    return render(request, 'auth_login.html', context)

# --- VISTAS DE GESTIÓN DE TAREAS (CORREGIDAS) ---

@login_required 
def tareas_list(request):
    """Muestra la lista de tareas del usuario autenticado, obtenidas de la memoria."""
    user_id = request.user.id
    
    tasks = get_user_tasks(user_id)
    
    context = {
      
        'tareas': tasks,
    }
    
    return render(request, 'tareas_list.html', context) 

@login_required 
def tarea_add(request):
    """Permite al usuario agregar una nueva tarea a la lista en memoria."""
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            tasks = get_user_tasks(user_id)
            
         
            new_task = {
                'id': get_next_task_id(),
                'title': form.cleaned_data['titulo'],
                'description': form.cleaned_data['descripcion'],
                'user_id': user_id
            }
            
            tasks.append(new_task)
            messages.success(request, f"Tarea '{new_task['title']}' agregada.")
            return redirect('tareas_list')
    else:
        form = TareaForm()
        
    context = {'form': form, 'title': 'Agregar Nueva Tarea'}
    return render(request, 'tarea_add.html', context)

@login_required
def tarea_detail(request, pk):
    """Muestra los detalles de una tarea, verificando que pertenezca al usuario."""
    user_id = request.user.id
    task_id = pk
    
    tarea = get_task_by_id(user_id, task_id)
    
    if tarea is None:
        raise PermissionDenied("Tarea no encontrada o no te pertenece.")
        
    context = {'tarea': tarea}
    return render(request, 'detalles_de_tarea.html', context)

@login_required
def tarea_delete(request, pk):
    """Permite al usuario eliminar una tarea existente, verificando pertenencia."""
    user_id = request.user.id
    tasks = get_user_tasks(user_id)
    task_id = pk
    
    tarea_to_delete = get_task_by_id(user_id, task_id)
    
    if tarea_to_delete is None:
        raise PermissionDenied("Tarea no encontrada o no te pertenece.")
    
    if request.method == 'POST':
       
        IN_MEMORY_TASKS[str(user_id)] = [t for t in tasks if t['id'] != task_id]

        messages.success(request, f"Tarea '{tarea_to_delete['title']}' eliminada.")
        return redirect('tareas_list')

   
    context = {'tarea': tarea_to_delete}
    return render(request, 'eliminar_tarea.html', context)