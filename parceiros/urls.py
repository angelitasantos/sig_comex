from django.urls import path
from .views import (ParceiroView, CategoriaView, GrupoView)


app_name = 'parceiros'

urlpatterns = [
    path('parceiros/', ParceiroView.as_view(), name='parceiros'),
    path('categorias/', CategoriaView.as_view(), name='categorias'),
    path('grupos/', GrupoView.as_view(), name='grupos'),
]
