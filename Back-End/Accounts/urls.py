from django.urls import path
from . import views

name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register-page'),
    path('login/', views.LoginView.as_view(), name='login-page'),
    path('logout/', views.LogoutView.as_view(), name='logout-page'),
    path('profile/', views.ProfileView.as_view(), name='profile-page'),
    path('profile/change_password/', views.ChangePasswordView.as_view(), name='change-password'),
]

