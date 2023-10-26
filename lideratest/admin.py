from django.contrib import admin
from .models import Task, knowledge_base, MyUser, ResultadoLiderazgo

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

class knowledge_baseAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    pass

class MyUserAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    pass

class ResultadoLiderazgoAdmin(admin.ModelAdmin):
    # Agrega configuraciones específicas si es necesario
    pass

# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(knowledge_base, knowledge_baseAdmin)
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(ResultadoLiderazgo, ResultadoLiderazgoAdmin)