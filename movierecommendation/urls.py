"""
URL configuration for movierecommendation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from movierecommendation import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),  # Replace 'movies.urls' with your actual movies app URLconf
    path('', include('adminpanel.urls')),  # Replace 'adminpanel.urls' with your actual admin panel app URLconf
    path('adminsignin/', auth_views.LoginView.as_view(
        template_name='adminsignin.html', redirect_authenticated_user=True), name='adminsignin'),
   
   
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
