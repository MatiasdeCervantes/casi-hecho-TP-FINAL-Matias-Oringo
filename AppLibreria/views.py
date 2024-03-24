from django.shortcuts import render
from django.http import HttpResponse
from AppLibreria.models import clientes, subgeneros, autor
from AppLibreria.forms import ClientesFormulario, SubgenerosFormulario, AutoresFormulario, RegistroUsuario, FormularioEditar, AvatarFormulario
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def IniciarSesion(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():

            usuario = form.cleaned_data.get("username")
            contraseña = form.cleaned_data.get("password")

            user = authenticate(username=usuario, password=contraseña)

            if user:

                login(request, user)

                return render(request, "inicio.html", {"mensaje":f"Bienvenido {user}"})
            
        else:

            return render(request, "inicio.html", {"mensaje":"Datos ingresados no son correctos"})
    
    
    else:

        form = AuthenticationForm() 
    
    
    return render(request, "login.html", {"formulario":form})


def registro(request):

    if request.method == "POST":

        form = RegistroUsuario(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            form.save()
            return render(request, "Inicio.html", {"mensaje":"Usuario creado."})
        
    else:

        form = RegistroUsuario()

    return render(request, "registro.html", {"formulario":form})


@login_required
def agregar_avatar(request):

    if request.method == "POST":

        form = AvatarFormulario(request.POST, request.FILES)

        if form.is_valid():
            
            info = form.cleaned_data
            usuario_actual = User.objects.get(username=request.user)
            nuevo_avatar = Avatar(usuario=usuario_actual, imagen=info["imagen"])
            
            nuevo_avatar.save()
            return render(request, "Inicio.html", {"mensaje":"Has creado tu avatar."})
        
    else:

        form = AvatarFormulario()

    return render(request, "registro.html", {"formulario":form})


def editarUsuario(request):

    usuario = request.user

    if request.method == "POST":

        form = FormularioEditar(request.POST)

        if form.is_valid():

            info = form.cleaned_data

            usuario.email = info["email"]
            usuario.set_password(info["password1"])
            usuario.first_name = info["first_name"]
            usuario.last_name = info["last_name"]

            usuario.save()

            return render(request, "inicio.html", {"mensaje":"Usuario editado."})
    
    else:

        form = FormularioEditar(initial={
            "email":usuario.email,
            "first_name":usuario.first_name,
            "last_name":usuario.last_name,
        })
    
    return render(request, "editarPerfil.html", {"formulario":form, "usuario":usuario})



def inicio(request):

    
    return render(request, "inicio.html", {"mensaje":"Adentrate en el terror desconocido..."})


def ver_autores(request):

    return render(request, "ver_autores.html")

def ver_clientes(request):

    return render(request, "ver_clientes.html")

def ver_subgeneros(request):

    return render(request, "ver_subgeneros.html")

def buscar_cliente(request):

    if request.GET:
        nombre = request.GET["nombre"]
        cliente = clientes.objects.filter(nombre__icontains=nombre)

        mensaje = f"Buscando cliente {nombre}"

        return render(request, "buscar_cliente.html", {"mensaje":mensaje, "resultado":cliente})

    return render(request, "buscar_cliente.html")

def buscar_autor(request):

    if request.GET:
        nombre = request.GET["nombre"]
        autor_busqueda = autor.objects.filter(nombre__icontains=nombre)

        mensaje = f"Buscando autor {nombre}"

        return render(request, "buscar_autor.html", {"mensaje":mensaje, "resultado":autor_busqueda})

    return render(request, "buscar_autor.html")

def buscar_subgenero(request):

    if request.GET:
        subgenero = request.GET["subgenero"]
        subgenero_busqueda = subgeneros.objects.filter(subgenero__icontains=subgenero)

        mensaje = f"Buscando subgenero {subgenero}"

        return render(request, "buscar_subgenero.html", {"mensaje":mensaje, "resultado":subgenero_busqueda})

    return render(request, "buscar_subgenero.html")

#CRUD AUTOR

def crear_autor(request):
 
    if request.method == "POST":
        autores_formulario = AutoresFormulario(request.POST) # se almacena la info del form
        if autores_formulario.is_valid():
            autores_dic = autores_formulario.cleaned_data #se convierte en diccionario

            autor_nuevo = autor(nombre=autores_dic["nombre"])
            autor_nuevo.save()
            return render(request, "inicio.html")
    else:

        autores_formulario = AutoresFormulario()

    return render(request, "autores.html", {"formu": autores_formulario})



def leerAutor(request):

    autores = autor.objects.all()

    contexto = {"autors": autores}

    return render(request, "leerAutor.html", contexto)


def eliminarAutor(request, autorNombre):

    autor = Autor.objects.get(id=autorNombre)
    autor.delete()

    autores = Autor.object.all()

    contexto = {"autors": autores}

    return render(request, "leerAutor.html", contexto)


def editarAutor(request, autorNombre):

    autor = Autor.objects.get(id=autorNombre)

    if request.method == "POST":
        autores_formulario = AutoresFormulario(request.POST) 
        if autores_formulario.is_valid():
            autores_dic = autores_formulario.cleaned_data 

            autor.nombre = info["nombre"]

            autor_nuevo.save()
            return render(request, "inicio.html")
    else:

        autores_formulario = AutoresFormulario(initial={"nombre":autor.nombre})

    return render(request, "editarAutor.html", {"formu": autores_formulario, "nombre":autorNombre})


#CRUD CLIENTE

def crear_cliente(request):

    if request.method == "POST":
        clientes_formulario = ClientesFormulario(request.POST) # se almacena la info del form
        if clientes_formulario.is_valid():
            clientes_dic = clientes_formulario.cleaned_data #se convierte en diccionario
            cliente_nuevo = cliente(nombre=cliente_dic["nombre"], apellido=cliente_dic["apellido"], email=cliente_dic["email"])
            cliente_nuevo.save()
            return render(request, "inicio.html")
    else:

        clientes_formulario = ClientesFormulario()

    return render(request, "clientes.html", {"formu": clientes_formulario})


def leerClientes(request):

    clientes = cliente.objects.all()

    contexto = {"clients": clientes}

    return render(request, "leerCliente.html", contexto)


def eliminarCliente(request, clienteNombre):

    cliente = Cliente.objects.get(id=clienteNombre)
    cliente.delete()

    clientes = Cliente.object.all()

    contexto = {"clients": clientes}

    return render(request, "leerCliente.html", contexto)


def editarCliente(request, clienteNombre):

    cliente = Cliente.objects.get(id=clienteNombre)

    if request.method == "POST":
        autores_formulario = ClientesFormulario(request.POST) 
        if clientes_formulario.is_valid():
            clientes_dic = clientes_formulario.cleaned_data 

            cliente.nombre = info["nombre"]

            cliente_nuevo.save()
            return render(request, "inicio.html")
    else:

        clientes_formulario = ClientesFormulario(initial={"nombre":cliente.nombre})

    return render(request, "editarCliente.html", {"formu": clientes_formulario, "nombre":clienteNombre})

#CRUD SUBGENERO

def crear_subgenero(request):
    
    if request.method == "POST":
        subgenero_formulario = SubgenerosFormulario(request.POST) # se almacena la info del form
        if subgenero_formulario.is_valid():
            subgenero_dic = subgenero_formulario.cleaned_data #se convierte en diccionario
            subgenero_nuevo = subgenero(nombre=subgenero_dic ["nombre"])
            subgenero_nuevo.save()
            return render(request, "inicio.html")
    else:

        subgenero_formulario = SubgenerosFormulario()

    return render(request, "subgeneros.html", {"formu": subgenero_formulario})


def leerSubgeneros(request):

    subgeneros = subgenero.objects.all()

    contexto = {"subgenres": subgeneros}

    return render(request, "leerSubgenero.html", contexto)


def eliminarSubgenero(request, subgeneroNombre):

    subgenero = Subgenero.objects.get(id=subgeneroNombre)
    subgenero.delete()

    subgeneros = Subgenero.object.all()

    contexto = {"subgenres": subgeneros}

    return render(request, "leerSubgenero.html", contexto)


def editarSubgenero(request, subgeneroNombre):

    subgenero = Subgenero.objects.get(id=subgeneroNombre)

    if request.method == "POST":
        subgenero_formulario = SubgenerosFormulario(request.POST) 
        if subgenero_formulario.is_valid():
            subgenero_dic = subgenero_formulario.cleaned_data 

            subgenero.nombre = info["nombre"]

            subgenero_nuevo.save()
            return render(request, "inicio.html")
    else:

        subgenero_formulario = SubgenerosFormulario(initial={"nombre":subgenero.nombre})

    return render(request, "editarSubgenero.html", {"formu": subgenero_formulario, "nombre":subgeneroNombre})


def cerrar_sesion(request):

    logout(request)

    return render(request, "inicio.html", {"mensaje":"Has cerrado sesion con exito"})
