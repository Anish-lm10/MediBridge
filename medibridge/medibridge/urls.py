"""
URL configuration for medibridge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from patient_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('mainpage.urls')),
    path('patient/',include('patient_app.urls')),
    path('doctor/',include('doctor_app.urls')),
    path('new_meeting/', new_meeting, name='new_meeting'),  # Shared endpoint
    path('join_meeting/', join_meeting, name='join_meeting'),  # Shared endpoint
    path('social-auth/', include('social_django.urls', namespace='social')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
