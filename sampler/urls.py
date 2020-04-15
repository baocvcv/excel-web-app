from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.UploadFile, name='upload'),
    path('set-param/', views.SetParam, name='set-param'),
]