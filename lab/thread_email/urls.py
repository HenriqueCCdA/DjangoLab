from django.urls import path
from lab.thread_email import views


urlpatterns = [
    path('send/', views.send_email),
    path('send-th/', views.send_email_th),
    path('send-th/status/', views.email_status),
]
