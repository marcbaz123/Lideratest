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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
            return self.title + ' - by ' + self.user.username
    
class knowledge_base(models.Model):
    id_kbase = models.AutoField(primary_key=True, db_column='id')
    question = models.TextField()
    def __str__(self):
        return str(self.id_kbase)
    
class MyUser(models.Model):
    type_user = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
# Definir un receptor para la señal post_save del modelo User
@receiver(post_save, sender=User)
def create_myuser(sender, instance, created, **kwargs):
    if created:
        # Si se crea un nuevo usuario, crea automáticamente un objeto MyUser asociado
        MyUser.objects.create(user=instance)

# Conecta el receptor a la señal post_save
post_save.connect(create_myuser, sender=User)

class ResultadoLiderazgo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Asegúrate de importar User
    fecha = models.DateTimeField(auto_now_add=True)
    calificaciones = models.JSONField()
    resultado_final = models.CharField(max_length=255)
    
