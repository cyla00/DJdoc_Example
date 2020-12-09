from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('admin/', views.admin, name='admin'),
    path('moderation/', views.moderation, name='moderation'),
    path('update/<str:usr_id>/', views.update_usr, name='update_usr'),
    path('delete/<str:usr_id>/', views.delete_usr, name='delete_usr'),
]