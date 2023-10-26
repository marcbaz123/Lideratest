<<<<<<< HEAD
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
 #   path('superconverter/', views.super_userconverter, name='superconverter'),
]

=======
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
 #   path('superconverter/', views.super_userconverter, name='superconverter'),
]

>>>>>>> deefa0f0eebc8e33ba9235ad1f9deb8c01c96f55
