
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_assigned_to')

    def __str__(self):
        return self.title + ' - by ' + self.user.username

class MyUser(models.Model):
    type_user = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='myuser')
    academy_level = models.CharField(max_length=100, blank=True)
    job = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.user.username
    
class knowledge_base(models.Model):
    id_kbase = models.AutoField(primary_key=True, db_column='id', default=1)
    question = models.TextField()
    def __str__(self):
        return str(self.id_kbase)
    

# Definir un receptor para la señal post_save del modelo User
@receiver(post_save, sender=User)
def create_myuser(sender, instance, created, **kwargs):
    if created:
        # Si se crea un nuevo usuario, crea automáticamente un objeto MyUser asociado
        MyUser.objects.create(user=instance)

# Conectar el receptor a la señal post_save
post_save.connect(create_myuser, sender=User)

class ResultadoLiderazgo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    fecha = models.DateTimeField(auto_now_add=True)
    calificaciones = models.JSONField()
    resultado_final = models.CharField(max_length=255)
    total_orientacion_personas = models.FloatField(default=0.0) 
    total_orientacion_produccion = models.FloatField(default=0.0)  


class Clase(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    usuarios_habilitados = models.ManyToManyField(User, related_name='clases_habilitadas')


class ResultadosEvaluador(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    evaluador = models.ForeignKey(User, on_delete=models.CASCADE)
    calificaciones = models.JSONField()
    total_orientacion_personas = models.FloatField()
    total_orientacion_produccion = models.FloatField()
    resultado_final = models.CharField(max_length=255)
    completado = models.BooleanField(default=False)  # Campo para indicar si el usuario ha completado el test
    fecha = models.DateTimeField(null=True, blank=True)
    suma_orientacion = models.IntegerField(default=0)
    def __str__(self):
        return f'ResultadosEvaluador {self.id}'
