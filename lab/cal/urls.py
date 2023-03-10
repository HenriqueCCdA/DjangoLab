from django.urls import path
from lab.cal import views


urlpatterns = [
    path('<int:size>/', views.register),
    path('', views.list_tasks),
    path('number-of-threads/', views.number_of_threads),
]
