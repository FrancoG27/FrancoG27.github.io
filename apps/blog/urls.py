from django.urls import path, reverse_lazy
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, 
    PasswordResetConfirmView,PasswordResetCompleteView,PasswordChangeView,PasswordChangeDoneView)
from django.contrib.auth.decorators import login_required

app_name = "blog"
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('Expo2023/', views.Expo2023, name='Expo2023'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('perfil/', views.perfil, name='perfil'), 
    path('registro/', views.registrarUsuario, name='registro'),
    path('login/', LoginView.as_view(template_name='perfil/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='perfil/logout.html'), name='logout'),
    
    path('crear_post/', login_required(views.crearPost), name='crear_post'),   
    path('mostrar_post/<int:pk>', views.mostrarPost, name='mostrar_post'),
    path('administrar_posts/', views.administrarPosts, name='administrar_posts'),
    path('eliminar_post/<int:pk>', views.eliminarPost, name='eliminar_post'),
    path('actualizar_post/<int:pk>/', login_required(views.actualizarPost), name='actualizar_post'),

    path('administrar_categorias/', views.administrarCategorias, name='administrar_categorias'),
    path('agregar_categoria/', views.agregarCategoria, name='agregar_categoria'),
    path('actualizar_categoria/<int:pk>', views.actualizarCategoria, name='actualizar_categoria'),
    path('eliminar_categoria/<int:pk>', views.eliminarCategoria, name='eliminar_categoria'),
    
    path('administrar_eventos/', views.administrarEventos, name='administrar_eventos'),
    path('agregar_evento/', views.agregarEvento, name='agregar_evento'),
    path('actualizar_evento/<int:pk>', views.actualizarEvento, name='actualizar_evento'),
    path('eliminar_evento/<int:pk>', views.eliminarEvento, name='eliminar_evento'),
    
    path('administrar_usuarios/', views.administrarUsuarios, name='administrar_usuarios'),
    path('agregar_usuarios/', views.agregarUsuarios, name='agregar_usuarios'),
    path('actualizar_usuarios/<int:pk>', views.actualizarUsuarios, name='actualizar_usuarios'),
    path('eliminar_usuarios/<int:pk>', views.eliminarUsuarios, name='eliminar_usuarios'),

    path('reset_password/', PasswordResetView.as_view(template_name='resetpass/password_reset_form.html',success_url=reverse_lazy('blog:password_reset_done'), email_template_name='resetpass/password_reset_email.html'), name='password_reset'),
    path('reset_password_send/', PasswordResetDoneView.as_view(template_name='resetpass/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='resetpass/password_reset_confirm.html',success_url=reverse_lazy('blog:password_reset_complete')), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name='resetpass/password_reset_complete.html'), name='password_reset_complete'),
    
    path('cambiar_contraseña/', PasswordChangeView.as_view(template_name='resetpass/password_change_form.html',success_url=reverse_lazy('blog:password_change_done')), name='password_change'),
    path('cambiar_contraseña_completo/', PasswordChangeDoneView.as_view(template_name='resetpass/password_change_done.html'), name='password_change_done')


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
