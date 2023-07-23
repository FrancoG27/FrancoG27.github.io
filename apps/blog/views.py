from django.shortcuts import render, get_object_or_404, redirect

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Q
from django.contrib import messages

from .models import Post, Categoria, Evento, Usuarios
from .forms import PostForm, RegistrarForm, CategoriaForm, EventoForm, UsuariosForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required




# Create your views here.
def index(request):
    """ se muestra la pantalla de inicio con post y eventos, además contiene la logica de busqueda y filtros """
    cat= Categoria.objects.all()

    ordenar = request.GET.get('ordenar')
    if ordenar == 'mas antiguos primero':
        ordenar = 'fecha_creacion'
    else:
        ordenar = '-fecha_creacion'
    
    fecha = request.GET.get('fecha')
    categoria = request.GET.get('categoria')
    busqueda = request.GET.get('buscar')
    if busqueda:
        posts = Post.objects.filter(
            Q(titulo__icontains=busqueda)|
            Q(resumen__icontains=busqueda)|
            Q(texto__icontains=busqueda)|
            Q(categoria__nombre__icontains=busqueda)
        ).distinct().order_by(ordenar)
    else:
        posts = Post.objects.all().order_by(ordenar)
    
    if categoria and categoria != "Seleccione una categoria":
        posts = posts.filter(
            Q(categoria__nombre__contains=categoria)
        )
    if fecha:
        posts = posts.filter(
            Q(fecha_creacion=fecha)
        )

    eventos= Evento.objects.all().order_by('-fecha_creacion')
    posts.order_by('fecha_creacion')
    context={'post':posts, 'cat':cat, 'eventos':eventos}

    return render(request, 'index.html', context)

def nosotros(request):
    """ se recuperan usuarios y se los muestra por pantalla """
    usuarios = Usuarios.objects.all()
    superusuarios = usuarios.filter(es_superusuario=True)
    colaboradores = usuarios.filter(es_colaborador=True)
    usuarios_activos = usuarios.filter(activo=True)
    context={"usuarios":usuarios_activos, "superusuarios":superusuarios, "colaboradores":colaboradores}
    return render(request, 'nosotros.html', context)

def Expo2023(request):
    """ se muestra el template con info de contacto """
    return render(request, 'Expo2023.html',)



def contacto(request):
   
    return render(request, 'contacto.html',)

def perfil(request):
    """ se muestra info de usuario o enlaces para editar secciones segun permisos """
    return render(request, 'perfil/perfil.html',)

def registrarUsuario(request):
    """ logica de registro de usuario """
    if request.method == 'POST':
        form= RegistrarForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('blog:index')
        else:
            messages.success(request, f'Error al crear usuario: su contraseña debe contar con numeros, letras y al menos un caracter especial')
    else:
        form = RegistrarForm()

    context = {'form':form}
    return render(request, 'perfil/registro.html', context)



def crearPost(request):
    """ lógica para crear post y guardarlo en la base de datos """
   
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:

        # Obtener el perfil de usuario a través del atributo 'profile'
        usuario = request.user.profile

        if usuario.es_colaborador:
            if request.method == 'POST':
                post_form = PostForm(request.POST or None, request.FILES or None)
                if post_form.is_valid():
                    post_form.save()
                    return redirect('blog:index')
            else:
                post_form = PostForm()
        else:
            # Si el usuario no es colaborador, todavía proporcionamos el formulario
            post_form = PostForm()
    else:
        # Si el usuario no está autenticado, redirigir al inicio de sesión
        return redirect('login')

    return render(request, 'post/guardar_post.html', {'post_form': post_form})

def mostrarPost(request, pk):
    """ se muestra el template con un posteo y sus comentarios """
    post = get_object_or_404(Post, pk=pk)

    # context solo si se usan comentarios externos
    context ={'post':post}
    return render(request, 'post/mostrar_post.html', context)

def administrarPosts(request):
    """ se muestran los post creados con las opciones de editar, eliminar y crear """
    cat= Categoria.objects.all()
    posts = Post.objects.all().order_by('-fecha_creacion')
    context={'post':posts, 'cat':cat}
    return render(request, 'post/administrar_post.html', context)

def actualizarPost(request,pk):
    """ funcion para modificar un post creado """
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        post_form = PostForm(request.POST or None, request.FILES or None, instance=post)
        if post_form.is_valid():
        
            
            post.save()
            messages.success(request, f"Post: '{post.titulo}' actualizado")

            return redirect('blog:administrar_posts')
    else:
        post_form = PostForm(instance=post)

    context = {'post_form': post_form}
    return render(request, 'post/guardar_post.html', context)

def eliminarPost(request,pk):
    """ funcion para eliminar un post de la base de datos """
    post = get_object_or_404(Post, pk=pk)
    print("Post eliminado: ",post)
    post.delete()
    return redirect('blog:administrar_posts')

### CRUD Categoria

def administrarCategorias(request):
    """ se muestran las categorias creadas con las opciones de editar, eliminar y crear """
    categorias= Categoria.objects.all()
    context={'categorias':categorias}
    return render(request, 'categoria/administrar_categorias.html', context)

def agregarCategoria(request):
    """ toma los compos del form para crear una categoria y guardarla en la base de datos """
    if request.method == 'POST':
        categoria_form = CategoriaForm(request.POST or None)
        if categoria_form.is_valid():
            categoria_form.save()
            messages.success(request, f"Categoria: '{categoria_form.cleaned_data['nombre']}' creada.")
            return redirect('blog:administrar_categorias')
    else:
        categoria_form = CategoriaForm()
    context={'categoria_form': categoria_form}
    return render(request, 'categoria/guardar_categoria.html', context)

def actualizarCategoria(request,pk):
    """ recupera la categoria por su id y actualiza los campos modificados """
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        categoria_form = CategoriaForm(request.POST or None, instance=categoria)
        if categoria_form.is_valid():
            # categoria.nombre=categoria_form.cleaned_data['nombre']

            categoria.save()
            messages.success(request, f"Categoria: '{categoria.nombre}' actualizada.")
            return redirect('blog:administrar_categorias')
    else:
        categoria_form = CategoriaForm(instance=categoria)

    context = {'categoria_form': categoria_form}
    return render(request, 'categoria/guardar_categoria.html', context)

def eliminarCategoria(request,pk):
    """ recupera la categoria por su id y la elimina """
    categoria = get_object_or_404(Categoria, pk=pk)
    print("Categoria eliminada: ",categoria)
    nombre_categoria = categoria.nombre
    categoria.delete()
    messages.success(request, f"Categoria '{nombre_categoria}' eliminada.")
    return redirect('blog:administrar_categorias')

### CRUD Evento

def administrarEventos(request):
    """ se muestran las categorias creadas con las opciones de editar, eliminar y crear """
    eventos= Evento.objects.all()
    context={'eventos':eventos}
    return render(request, 'evento/administrar_eventos.html', context)

def agregarEvento(request):
    """ toma los compos del form para crear un evento y guardarlo en la base de datos """
    if request.method == 'POST':
        evento_form = EventoForm(request.POST or None)
        if evento_form.is_valid():
            evento_form.save()
            messages.success(request, f"Nuevo evento creado: '{evento_form.cleaned_data['titulo']}'.")
            return redirect('blog:administrar_eventos')
    else:
        evento_form = EventoForm()
    context={'evento_form': evento_form}
    return render(request, 'evento/guardar_evento.html', context)

def actualizarEvento(request,pk):
    """ recupera el evento por id y actualiza los campos modificados """
    evento = get_object_or_404(Evento, pk=pk)
    
    if request.method == 'POST':
        evento_form = EventoForm(request.POST or None, instance=evento)
        if evento_form.is_valid():
            # evento.titulo=evento_form.cleaned_data['titulo']
            # evento.descripcion=evento_form.cleaned_data['descripcion']

            evento.save()
            messages.success(request, f"Evento '{evento.titulo}' actualizado.")
            return redirect('blog:administrar_eventos')
    else:
        evento_form = EventoForm(instance=evento)

    context = {'evento_form': evento_form}
    return render(request, 'evento/guardar_evento.html', context)

def eliminarEvento(request,pk):
    """ recupera el evento por su id y lo elimina de la base de datos"""
    evento = get_object_or_404(Evento, pk=pk)
    print("Evento eliminado: ",evento)
    nombre_evento = evento.titulo
    evento.delete()
    messages.success(request, f"Evento '{nombre_evento}' eliminado.")
    return redirect('blog:administrar_eventos')

### CRUD usuarios

def administrarUsuarios(request):
    """ se muestran los usuarios creados con las opciones de editar, eliminar y crear """
    usuarios= Usuarios.objects.all()
    superusuarios = usuarios.filter(es_superusuario=True)
    colaboradores = usuarios.filter(es_colaborador=True)
    usuarios_activos = usuarios.filter(activo=True)
    context={"usuarios":usuarios_activos, "superusuarios":superusuarios, "colaboradores":colaboradores}
    return render(request, 'usuarios/administrar_usuarios.html', context)

def agregarUsuarios(request):
    """ toma los compos del form para crear un usuarios y guardarlo en la base de datos """
    if request.method == 'POST':
        usuarios_form = UsuariosForm(request.POST or None, request.FILES or None)
        if usuarios_form.is_valid():
            print('llegue')
            usuarios_form.save()
            messages.success(request, f"Nuevo usuario creado: '{usuarios_form.cleaned_data['apellido']}, {usuarios_form.cleaned_data['primer_nombre']} {usuarios_form.cleaned_data['segundo_nombre']}'.")
            return redirect('blog:administrar_usuarios')
    else:
        usuarios_form = UsuariosForm()
    context={'usuarios_form': usuarios_form}
    return render(request, 'usuarios/guardar_usuarios.html', context)

def actualizarUsuarios(request,pk):
    """ recupera el usuario por id y actualiza los campos modificados """
    usuarios = get_object_or_404(Usuarios, pk=pk)
    
    if request.method == 'POST':
        usuarios_form = UsuariosForm(request.POST or None, request.FILES or None, instance=usuarios)
        if usuarios_form.is_valid():
          
            
            usuarios.save()
            messages.success(request, f"Usuario '{usuarios.apellido}, {usuarios.primer_nombre} {usuarios.segundo_nombre}' actualizado.")
            return redirect('blog:administrar_usuarios')
    else:
       usuarios_form = UsuariosForm(instance=usuarios)

    context = {'usuarios_form': usuarios_form}
    return render(request, 'usuarios/guardar_usuarios.html', context)

def eliminarUsuarios(request,pk):
    """ recupera el Usuarios por su id y lo elimina de la base de datos"""
    usuarios = get_object_or_404(Usuarios, pk=pk)
    print("Usuario eliminado: ",usuarios)
    nombre_usuarios = usuarios.primer_nombre + usuarios.segundo_nombre
    apellido_usuarios = usuarios.apellido
    usuarios.delete()
    messages.success(request, f"Usuario '{apellido_usuarios}, {nombre_usuarios}' eliminado.")
    return redirect('blog:administrar_usuarios')