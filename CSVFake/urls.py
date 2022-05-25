"""CSVFake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from schema.views import create_column
from schema.views import list_schema, listFilesAndDownload
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(list_schema), name = 'listschema'),
    path('list/', login_required(list_schema)),
    path('listfiles/', login_required(listFilesAndDownload), name='listfiledownload'),
    path('schema/', include('schema.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('celery-progress/', include('celery_progress.urls')),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]

urlpatterns+= (static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) +
                  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
