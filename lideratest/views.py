import datetime
from django import template
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import Taskform, UserProfileUpdateForm, ClaseForm
from .models import Clase, MyUser, ResultadoLiderazgo, ResultadosEvaluador, Task, knowledge_base
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
def is_type_user_1(user):
    return user.myuser.type_user == 1
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

            return redirect('home')
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
    
    resultado = ""  # Agrega la definición de la variable resultado

    if request.method == 'POST':
        total_orientacion_personas = 0
        total_orientacion_produccion = 0
        calificaciones = {}  # Crear un diccionario para almacenar calificaciones

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

            # Almacena las calificaciones junto con las preguntas
            pregunta = preguntas.get(id_kbase=i)
            calificaciones[pregunta.question] = respuesta

        total_orientacion_personas *= 0.2
        total_orientacion_produccion *= 0.2
        
         # Llamada al motor de inferencia
        engine = MotorLiderazgo()
        engine.reset()
        engine.declare(EstiloLiderazgo(total_orientacion_personas=total_orientacion_personas, total_orientacion_produccion=total_orientacion_produccion))
        engine.run()
        resultado = engine.resultado
        
        # Calcular el resultado
        if not resultado:
            if total_orientacion_produccion > total_orientacion_personas:
                resultado = "Resultados inconcluyentes Con tendencias hacia Centrado a Produccion"
            elif total_orientacion_personas > total_orientacion_produccion:
                resultado = "Resultados inconcluyentes Con tendencias hacia Centrado a Personas"
            elif total_orientacion_personas == 5 and total_orientacion_produccion == 5:
                resultado = "Resultado indefinido sin tendencias a social o autoritario"

        # Guardar los resultados en la base de datos
        resultado_liderazgo = ResultadoLiderazgo(
            user=request.user,  # Asigna el usuario actual
            calificaciones=calificaciones,  # Asigna el diccionario de calificaciones
            resultado_final=resultado,  # Asigna el resultado final
            total_orientacion_personas=total_orientacion_personas,  # Asigna el total_orientacion_personas
            total_orientacion_produccion=total_orientacion_produccion  # Asigna el total_orientacion_produccion
        )
        resultado_liderazgo.save()

        # Recuperar los resultados de la base de datos
        resultados = ResultadoLiderazgo.objects.filter(user=request.user)

        # Aquí puedes hacer lo que necesites con el resultado, como guardarlo en la base de datos o mostrarlo en la plantilla.
        return render(request, 'test_result.html', {'resultado_liderazgo': resultado, 'resultados': resultados, 'preguntas': preguntas})
    else:
        # Si el formulario no se ha enviado, simplemente muestra el formulario HTML.
        return render(request, 'expert.html', {'preguntas': preguntas})

def contact_admin(request):
    if request.method == 'POST':
        user = request.user
        subject = request.POST['subject']
        message = request.POST['message']
        from_email = user.email  # Obtenemos el correo del usuario logueado
        recipient_list = ['marcbaz1998@gmail.com']  # Cambia esto a tu dirección de correo

        try:
            full_message= f"Usuario : {user.username}\n\n{message}"
            send_mail(subject, full_message, from_email, recipient_list, fail_silently=False)
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

@login_required
def crear_clase(request):
    if request.method == 'POST':
        # Si se envió un formulario POST, procesa los datos
        form = ClaseForm(request.POST)  # Utiliza tu formulario para crear clases

        if form.is_valid():
            # Si el formulario es válido, crea una nueva clase
            nueva_clase = form.save(commit=False)
            nueva_clase.creador = request.user  # Asigna al usuario actual como el creador
            nueva_clase.save()

            # Agregar el creador a la lista de usuarios habilitados
            nueva_clase.usuarios_habilitados.add(request.user)
            nueva_clase.save()

            # Redirige a la página de detalle de la clase recién creada o a donde desees
            return redirect('habilitar_usuarios', clase_id=nueva_clase.id)
    else:
        # Si es una solicitud GET, muestra el formulario para crear clases
        form = ClaseForm()  # Utiliza tu formulario para crear clases

    return render(request, 'crear_clase.html', {'form': form})
 

def habilitar_usuarios(request, clase_id):
    clase = get_object_or_404(Clase, pk=clase_id)
    
    usuarios_disponibles = User.objects.exclude(pk=request.user.pk)
    usuarios_habilitados = clase.usuarios_habilitados.all()
    
    if request.method == 'POST':
        try:
            # Procesar el formulario y habilitar usuarios seleccionados
            usuarios_habilitados_ids = request.POST.getlist('usuarios_habilitados')
            clase.usuarios_habilitados.set(usuarios_habilitados_ids)

            # Agregar un mensaje de éxito
            messages.success(request, 'Usuarios habilitados con éxito.')

        except Exception as e:
            # En caso de error, agregar un mensaje de error
            messages.error(request, 'Ocurrió un error al habilitar usuarios: {}'.format(str(e)))

    return render(request, 'habilitar_usuarios.html', {
        'clase': clase,
        'usuarios_disponibles': usuarios_disponibles,
        'usuarios_habilitados': usuarios_habilitados
    })
    
@login_required
def detalle_clase(request, clase_id):
    clase = get_object_or_404(Clase, pk=clase_id)
    # Aquí puedes agregar cualquier lógica adicional que desees para mostrar detalles de la clase
    if request.user not in clase.usuarios_habilitados.all():
        return redirect('home')
    else:
        return render(request, 'detalle_clase.html', {'clase': clase})

@login_required
def clases_habilitadas(request):
    user = request.user
    clases_habilitadas = Clase.objects.filter(usuarios_habilitados=user)
    return render(request, 'clases_habilitadas.html', {'clases_habilitadas': clases_habilitadas})

@login_required
def expert_test(request, clase_id):
    clase = get_object_or_404(Clase, pk=clase_id)

    # Verifica si el usuario actual está habilitado para tomar el test en esta clase
    if request.user in clase.usuarios_habilitados.all():
        preguntas = knowledge_base.objects.all().order_by('id_kbase')
        resultado_evaluador = ResultadosEvaluador.objects.filter(evaluador=request.user, clase=clase).first()

        if resultado_evaluador is not None and resultado_evaluador.completado:
            # Mostrar el mensaje "Ya completaste el formulario"
            return HttpResponse("Ya completaste el formulario")

        if request.method == 'POST':
            total_orientacion_personas = 0
            total_orientacion_produccion = 0
            calificaciones = {}

            for i in range(1, 19):
                respuesta = request.POST.get(f"respuesta_{i}")
                if respuesta is not None:
                    respuesta = int(respuesta)
                else:
                    respuesta = 0

                if i in [1, 4, 6, 9, 10, 12, 14, 16, 17]:
                    total_orientacion_personas += respuesta
                else:
                    total_orientacion_produccion += respuesta

                pregunta = preguntas.get(id_kbase=i)
                calificaciones[pregunta.question] = respuesta

            total_orientacion_personas *= 0.2
            total_orientacion_produccion *= 0.2

           

            engine = MotorLiderazgo()
            engine.reset()
            engine.declare(EstiloLiderazgo(total_orientacion_personas=total_orientacion_personas, total_orientacion_produccion=total_orientacion_produccion))
            engine.run()
            resultado = engine.resultado

            if not resultado:
                if total_orientacion_produccion > total_orientacion_personas:
                    resultado = "Resultados inconcluyentes Con tendencias hacia Centrado a Produccion"
                elif total_orientacion_personas > total_orientacion_produccion:
                    resultado = "Resultados inconcluyentes Con tendencias hacia Centrado a Personas"
                elif total_orientacion_personas == 5 and total_orientacion_produccion == 5:
                    resultado = "Resultado indefinido sin tendencias a social o autoritario"

            # Guardar los resultados en ResultadosEvaluador
            resultado_evaluador = ResultadosEvaluador(
                clase=clase,  # Asigna la clase actual
                evaluador=request.user,  # Asigna el usuario que realiza el test
                calificaciones=calificaciones,
                resultado_final=resultado,
                total_orientacion_personas=total_orientacion_personas,
                total_orientacion_produccion=total_orientacion_produccion,
                fecha= datetime.datetime.now(),
                completado=True  ,
                suma_orientacion = total_orientacion_personas + total_orientacion_produccion
            )
            resultado_evaluador.save()

            resultados = ResultadosEvaluador.objects.filter(evaluador=request.user, clase=clase)

            return render(request, 'test_result.html', {'resultado_evaluador': resultado, 'resultados': resultados, 'preguntas': preguntas})
        else:
            return render(request, 'expert_test.html', {'preguntas': preguntas, 'clase': clase})
    else:
        return redirect('home')  # Agregar que si completado es = false que se haga todo esto pero sino que ponga de mensaje "Ya completaste el formulario"

    

@login_required
def clase_completada(request, clase_id):
    clase = get_object_or_404(Clase, pk=clase_id)

    # Verifica si el usuario actual (profesor) está habilitado para esta clase
    if request.user == clase.creador or request.user in clase.usuarios_habilitados.all():
        # Filtrar todos los resultados de evaluador para esta clase
        resultados_clase = ResultadosEvaluador.objects.filter(clase=clase)

        resultados_con_info_usuario = []  # Aquí almacenaremos todos los resultados con información de usuario

        for resultado in resultados_clase:
            evaluador_info = {
                'evaluado': resultado.evaluador,
                'nombre': resultado.evaluador.first_name,  # Nombre del usuario
                'apellido': resultado.evaluador.last_name,  # Apellido del usuario
                'correo': resultado.evaluador.email,  # Correo del usuario
                'resultado': resultado.resultado_final,
                'fecha': resultado.evaluador.date_joined,
                'calificaciones': resultado.calificaciones,
                'total_orientacion_personas': resultado.total_orientacion_personas,
                'total_orientacion_produccion': resultado.total_orientacion_produccion,
            }
            resultados_con_info_usuario.append(evaluador_info)

        # Ordena los resultados por la suma de orientación en orden descendente
        resultados_con_info_usuario = sorted(resultados_con_info_usuario, key=lambda x: x['total_orientacion_personas'] + x['total_orientacion_produccion'], reverse=True)

        return render(request, 'clase_completada.html', {'clase': clase, 'resultados_con_info_usuario': resultados_con_info_usuario})
    else:
        raise Http404("No tienes permiso para acceder a esta página")

    

@login_required
def clases_panel(request):
    user = request.user
    type_user = user.myuser.type_user  # Asume que el tipo de usuario está almacenado en user.myuser.type_user

    if type_user == 0:
        # Si el usuario es de tipo 0, muestra las clases habilitadas para los estudiantes
        clases_habilitadas = Clase.objects.filter(usuarios_habilitados=user)
        template_name = 'clases_habilitadas.html'
    else:
        # Si el usuario no es de tipo 0 (por ejemplo, profesor), muestra las clases de su panel
        clases_habilitadas = Clase.objects.filter(creador=user)
        template_name = 'clases_panel.html'

    return render(request, template_name, {'clases_habilitadas': clases_habilitadas})
