from django.db import models


class Ativo(models.Model):
    nome = models.CharField(max_length=10)
    sigla = models.CharField(max_length=2)

    def __str__(self):
        return self.nome
