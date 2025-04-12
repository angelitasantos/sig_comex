from django.urls import path
from .views import (ParceiroView)


app_name = 'parceiros'

urlpatterns = [
    path('parceiros/', ParceiroView.as_view(), name='parceiros'),
]
