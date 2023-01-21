from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('norm/', include('lab.cal.urls')),
    path('email/', include('lab.thread_email.urls')),
]
