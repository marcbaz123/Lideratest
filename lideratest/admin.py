from django.contrib import admin
from .models import Task, MyUser, knowledge_base, ResultadoLiderazgo, Clase, ResultadosEvaluador

# Define las clases de administración si es necesario
#class TaskAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
 #   pass

class MyUserAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    pass

class knowledge_baseAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    pass
#class ResultadoLiderazgoAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
 #   pass
class ClaseAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    pass

class ResultadosEvaluadorAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    pass

# Registra los modelos en el panel de administración
#admin.site.register(Task, TaskAdmin)
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(knowledge_base, knowledge_baseAdmin)
#admin.site.register(ResultadoLiderazgo, ResultadoLiderazgoAdmin)
admin.site.register(Clase, ClaseAdmin)
admin.site.register(ResultadosEvaluador, ResultadosEvaluadorAdmin)
