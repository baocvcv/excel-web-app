from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'sampler'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:doc_id>/setparam/', views.SetParam, name='do-sampling'),
]