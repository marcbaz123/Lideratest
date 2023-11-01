from django.contrib import admin
from .models import Task, MyUser, knowledge_base, ResultadoLiderazgo, Clase, ResultadosEvaluador

# Define las clases de administración si es necesario
class TaskAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    list_display = ['title', 'description', 'created', 'datecompleted', 'important', 'user', 'assigned_to']

class MyUserAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    list_display = ['user', 'type_user']

class knowledge_baseAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    list_display = ['id_kbase', 'question']

class ResultadoLiderazgoAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    list_display = ['user', 'fecha', 'calificaciones', 'resultado_final', 'total_orientacion_personas', 'total_orientacion_produccion']

class ClaseAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    list_display = ['nombre', 'descripcion', 'creador', 'completada']

class ResultadosEvaluadorAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    list_display = ['clase', 'evaluador', 'calificaciones', 'total_orientacion_personas', 'total_orientacion_produccion', 'resultado_final', 'completado', 'suma_orientacion']

# Registra los modelos en el panel de administración
admin.site.register(Task, TaskAdmin)
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(knowledge_base, knowledge_baseAdmin)
admin.site.register(ResultadoLiderazgo, ResultadoLiderazgoAdmin)
admin.site.register(Clase, ClaseAdmin)
admin.site.register(ResultadosEvaluador, ResultadosEvaluadorAdmin)
