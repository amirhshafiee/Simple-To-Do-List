from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.ShowTasksView.as_view(), name='show-all-task'),
    path('home/<int:pk>/', views.ShowTaskView.as_view(), name='show-one-task'),
]