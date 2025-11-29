from django import forms
from .models import Tarea

class TareaForm(forms.ModelForm):
    """
    Formulario para agregar una tarea, basado en el modelo Tarea.
    """
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Comprar leche'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalles de la tarea'}),
        }
        labels = {
            'titulo': 'Título de la Tarea',
            'descripcion': 'Descripción',
        }