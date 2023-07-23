from django.contrib import admin
from .models import *

class CategoriaAdmin(admin.ModelAdmin):
    ordering = ('id', 'nombre', 'activado', 'fecha_creacion')
    search_fields = ('id', 'nombre', 'activado', 'fecha_creacion')
    list_display = ('id', 'nombre', 'activado', 'fecha_creacion')
    list_filter = ('activado',)

class PostAdmin(admin.ModelAdmin):
    ordering = ('id', 'titulo', 'resumen', 'texto', 'imagen', 'categoria__nombre', 'publicado', 'fecha_creacion', 'usuario')
    search_fields = ('id', 'titulo', 'resumen', 'texto', 'imagen', 'categoria__nombre', 'publicado', 'fecha_creacion')
    list_display = ('titulo', 'resumen', 'imagen', 'categoria', 'publicado', 'fecha_creacion', 'usuario')
    list_filter = ('categoria__nombre', 'publicado')


class EventoAdmin(admin.ModelAdmin):
    ordering = ('id', 'titulo', 'descripcion', 'fecha_creacion', 'usuario__username')
    search_fields = ('id', 'titulo', 'descripcion', 'fecha_creacion')
    list_display = ('titulo', 'descripcion', 'fecha_creacion', 'usuario')
    list_filter = ('id', 'titulo', 'descripcion', 'fecha_creacion', 'usuario__username')

class UsuariosAdmin(admin.ModelAdmin):
    ordering = ('id', 'primer_nombre', 'segundo_nombre', 'apellido', 'fecha_nacimiento', 'imagen','biografia','activo','es_colaborador','es_superusuario')
    search_fields = ('id', 'primer_nombre', 'segundo_nombre', 'apellido', 'fecha_nacimiento', 'activo','es_colaborador','es_superusuario')
    list_display = ('primer_nombre', 'segundo_nombre', 'apellido', 'fecha_nacimiento', 'imagen','activo','es_colaborador','es_superusuario')
    list_filter = ('activo','es_colaborador','es_superusuario')



admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Usuarios, UsuariosAdmin)
