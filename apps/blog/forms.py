from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from django.forms.forms import Form
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'resumen', 'texto', 'imagen', 'categoria', 'usuario']

class RegistrarForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir Contraseña', widget=forms.PasswordInput)

    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo','descripcion','usuario']

class UsuariosForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['user','primer_nombre','segundo_nombre','apellido', 'fecha_nacimiento', 'imagen','biografia','activo','es_colaborador','es_superusuario']
