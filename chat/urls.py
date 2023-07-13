from django.urls import path
from django.contrib.auth import views as auth_views
from chat import views

app_name = 'chat'
urlpatterns = [
    # Chat
    path('', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout')
]
