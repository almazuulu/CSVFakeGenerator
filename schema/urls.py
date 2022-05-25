from django.urls import include, path
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('createschema/', login_required(create_schema), name = 'create-schema'),
    path('<pk>/', login_required(create_column), name = 'create-column'),
    path('htmx/column-form/',login_required(create_column_form), name='column-form'),
    path('htmx/column/<pk>/',login_required(detail_column), name='detail-column'),
    path('htmx/schema/<pk>/delete',login_required(delete_scheme), name='delete-scheme'),
    path('htmx/schema/<pk>/edit',login_required(edit_scheme), name='edit-scheme'),
    path('generatecsv/<pk>/',login_required(generate_csv), name="generate-csv"),
    path('generatefile/<pk>/',login_required(generatefilecsv), name="generate-file"),
    path('downloadcsv/<str:filename>', login_required(downloadFileCsv), name='downloadcsv')
]