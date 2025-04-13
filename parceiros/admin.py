from django.contrib import admin
from .models import (Ativo, Categoria, Grupo, Parceiro)

admin.site.register(Ativo)
admin.site.register(Categoria)
admin.site.register(Grupo)
admin.site.register(Parceiro)
