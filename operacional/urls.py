from django.urls import path
from .views import (OperacionalView, ImportaDadosView,
                    ImportaParceiroView, ImportaParceiroAlteradoView,
                    ExportaDadosView)

app_name = 'operacional'

urlpatterns = [
     path('operacional/', OperacionalView.as_view(), name='operacional'),

     path('importardados/', ImportaDadosView.as_view(),
          name='importar_dados'),

     path('importarparceiros/', ImportaParceiroView.as_view(),
          name='importar_parceiros'),
     path('importarparceirosalterados/', ImportaParceiroAlteradoView.as_view(),
          name='importar_parceiros_alterados'),

     path('exportardados/',
          ExportaDadosView.as_view(), name='exportar_dados'),
]
