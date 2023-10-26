from django.http import Http404, HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import Taskform, UserProfileUpdateForm
from .models import ResultadoLiderazgo, Task, knowledge_base
from django.contrib.auth.decorators import login_required
from .motor_inferencia import EstiloLiderazgo, MotorLiderazgo
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
# Create your views here.
def home(request):
     # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        try:
            # Obtén el último resultado de liderazgo del usuario actual
            resultado_liderazgo = ResultadoLiderazgo.objects.filter(user=request.user).latest('fecha')
        except ResultadoLiderazgo.DoesNotExist:
            resultado_liderazgo = None

        return render(request, "home.html", {'resultado_liderazgo': resultado_liderazgo})
    else:
        # Si el usuario no está autenticado, redirige a la página de inicio de sesión (signin)
        return redirect('signin')


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {'form': UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                    email=request.POST["email"],  # Agrega esta línea para el email
                    first_name=request.POST["first_name"],  # Agrega esta línea para el primer nombre
                    last_name=request.POST["last_name"],  # Agrega esta línea para el apellido
                   
                
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, "signup.html", {
                    'form': UserCreationForm,
                    'error': "User Already Exists",
                })
   
            
        return render(request, "signup.html", {
            'form': UserCreationForm,
            'error': "Password do not match"
            })

@login_required
def update_profile(request):
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()

            # Actualiza la sesión del usuario si se ha cambiado la contraseña
            password = form.cleaned_data['password']
            if password:
                user.set_password(password)
                user.save()
                # Asegura que la sesión del usuario siga siendo válida después de cambiar la contraseña
                update_session_auth_hash(request, user)

            return redirect('tasks')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    return render(request, "update_profile.html", {'form': form})
    
@login_required
def tasks (request):
    tasks = Task.objects.filter(user= request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    if request.user.is_authenticated:
        # Verificar el tipo de usuario (asumiendo que 1 representa "evaluador")
        if request.user.myuser.type_user ==1:
            tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
            return render(request, 'tasks.html', {'tasks': tasks})
        else:
            raise Http404("No estás autorizado para ver esta página")
            # Realizar acciones específicas para otros tipos de usuarios
            # Por ejemplo, redirigirlos a una página de acceso no autorizado.
            
    else:
        # Realizar acciones para usuarios no autenticados
        # Por ejemplo, redirigirlos a la página de inicio de sesión.
        return redirect('login')
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',
        {
                'form': Taskform
        })
    else:
        try:
            form = Taskform(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',
            {
                'form': Taskform,
                'error':'Please provide valida data'
            })
@login_required        
def task_detail(request, task_id): 
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        form = Taskform(instance=task)
        return render(request, 'task_detail.html',{'task':task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id)
            form = Taskform(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',{'task':task, 'form': form,
            'error' : "Error updating taks "})
    

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user) 
    if request.method == 'POST':
        task.datecompleted = timezone.now()  
        task.save()
        return redirect('tasks')
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user) 
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required                       
def signuot(request):
    logout(request)
    return  redirect('home')

def politicas(request):
  return render(request,'politicas.html')  

@login_required
def informacion(request):
  return render(request,'informacion.html')  
    
def signin(request):
    if request.method == 'GET':
         return render(request, 'signin.html',{
            'form' : AuthenticationForm
    })
    else:
        user =  authenticate(
            request, username=request.POST['username'],
            password=request.POST['password'])
        if user is None:
             return render(request, 'signin.html',{
            'form' : AuthenticationForm,
            'error' : 'User name or password is incorrect'
        })
        else:

            login(request, user)
            return redirect('home')
        

@login_required
def expert(request):
    # Obtén todas las preguntas del modelo knowledge_base
    preguntas = knowledge_base.objects.all().order_by('id_kbase')
    if request.method == 'POST':
        total_orientacion_personas = 0
        total_orientacion_produccion = 0
        for i in range(1, 19):
            respuesta = request.POST.get(f"respuesta_{i}")
            if respuesta is not None:
                respuesta = int(respuesta)
               
            else:
                respuesta = 0  # O cualquier otro valor por defecto que desees si no hay respuesta.
              
            if i in [1, 4, 6, 9, 10, 12, 14, 16, 17]:
                total_orientacion_personas += respuesta
            else:
                total_orientacion_produccion += respuesta
                
        print('Total orientacion produccion', total_orientacion_produccion)
        print('Total orientacion person', total_orientacion_personas)
        total_orientacion_personas *= 0.2
        total_orientacion_produccion *= 0.2
        print('Total orientacion produccion', total_orientacion_produccion)
        print('Total orientacion person', total_orientacion_personas)
        engine = MotorLiderazgo()
        engine.reset()
        engine.declare(EstiloLiderazgo(total_orientacion_personas=total_orientacion_personas, total_orientacion_produccion=total_orientacion_produccion))
        engine.run()
        resultado = engine.resultado
        print(resultado)

        if total_orientacion_produccion > total_orientacion_personas:
            resultado = "Resultados inconcluyentes Con tendencias hacia Centrado a Produccion"
        elif total_orientacion_personas > total_orientacion_produccion:
            resultado = "Resultados inconcluyentes Con tendencias hacia Centrado a Personas"
        elif total_orientacion_personas == 5 and total_orientacion_produccion == 5:
            resultado = "Resultado indefinido sin tendencias a social o autoritario"

        # Guardar los resultados en la base de datos
        resultado_liderazgo = ResultadoLiderazgo(
        user=request.user,  # Asigna el usuario actual
        calificaciones={f"respuesta_{i}": int(request.POST.get(f"respuesta_{i}", 0)) for i in range(1, 19)},
        resultado_final=resultado  # Asigna el resultado final
    )
        resultado_liderazgo.save()
        # Recuperar los resultados de la base de datos
        resultados = ResultadoLiderazgo.objects.filter(user=request.user)

        # Aquí puedes hacer lo que necesites con el resultado, como guardarlo en la base de datos o mostrarlo en la plantilla.
        return render(request, 'test_result.html', {'resultado_liderazgo': resultado, 'resultados': resultados, 'preguntas': preguntas})
    else:
        # Si el formulario no se ha enviado, simplemente muestra el formulario HTML.
        return render(request, 'expert.html',{'preguntas':preguntas})

def contact_admin(request):
    if request.method == 'POST':
        user = request.user
        subject = request.POST['subject']
        message = request.POST['message']
        from_email = user.email  # Obtenemos el correo del usuario logueado
        recipient_list = ['marcbaz1998@gmail.com']  # Cambia esto a tu dirección de correo

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            messages.success(request, 'Correo enviado con éxito. Gracias por contactarnos.')
        except:
            messages.error(request, 'Hubo un error al enviar el correo.')

        
    return render(request, 'contact_admin.html')

@login_required
def tutorial (request): 
    return render(request, 'tutorial_blake_mouton.html')

# def super_userconverter(request):
#    if request.method == 'POST':
#        selected_users = request.POST.getlist('selected_users')
 #       for username in selected_users:
  #          try:
   #             user = User.objects.get(username=username)
   #             user.is_superuser = True
    #            user.is_staff = True
     #           user.save()
      #          messages.success(request, f'{username} se ha convertido en superusuario.')
       #     except User.DoesNotExist:
        #        messages.error(request, f'El usuario {username} no existe.')
        #return redirect('superconverter')
    #
    #users = User.objects.all()
    #return render(request, 'super_userconverter.html', {'users': users})