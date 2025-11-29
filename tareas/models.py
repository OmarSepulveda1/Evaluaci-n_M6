from django.db import models
from django.contrib.auth.models import User

class Tarea(models.Model):
    """
    Modelo que representa una tarea en la base de datos.
    """
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    completada = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

