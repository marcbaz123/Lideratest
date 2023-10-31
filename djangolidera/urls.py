from django.contrib import admin
from django.urls import path  
from lideratest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('logout/', views.signuot, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('test_blake-mouton/', views.expert, name='expert'),
    path('contact/', views.contact_admin, name='contact_admin'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('tutorial_blake_mouton/', views.tutorial, name='tutorial'),
    path('politicas/', views.politicas, name='politicas'),
    path('informacion/', views.informacion, name='informacion'),
    path('crear_clase/', views.crear_clase, name='crear_clase'),
    path('clases/<int:clase_id>/habilitar/', views.habilitar_usuarios, name='habilitar_usuarios'),
    path('clases/<int:clase_id>/', views.detalle_clase, name='detalle_clase'),
    path('clases/', views.clases_habilitadas, name='clases'),
    path('lideratest/test_blake-mouton/', views.expert_test, name='expert_test'),
    path('clase_completada/', views.clase_completada, name='clase_completada'),
    path('expert_test/<int:clase_id>/', views.expert_test, name='expert_test'),
    path('clase_completada/<int:clase_id>/', views.clase_completada, name='clase_completada'),
    path('clases_panel/', views.clases_panel, name='clases_panel'),
    path('detalle_clase/', views.detalle_clase, name='detalle_clase'),
 #   path('superconverter/', views.super_userconverter, name='superconverter'),
]