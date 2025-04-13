from django.db import models


class Ativo(models.Model):
    nome = models.CharField(max_length=10)
    sigla = models.CharField(max_length=2)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=20)
    status = models.ForeignKey(Ativo, on_delete=models.SET_NULL,
                               null=True, blank=True)

    def __str__(self):
        return self.nome


class Grupo(models.Model):
    nome = models.CharField(max_length=20)
    status = models.ForeignKey(Ativo, on_delete=models.SET_NULL,
                               null=True, blank=True)

    def __str__(self):
        return self.nome


class Parceiro(models.Model):
    nome = models.CharField(
        max_length=30, verbose_name='NOME FANTASIA', null=True, blank=True)
    razao_social = models.CharField(
        max_length=100, verbose_name='RAZÃO SOCIAL', null=True, blank=True)
    cnpj = models.CharField(
        max_length=20, verbose_name='CNPJ', null=True, blank=True)
    insc_est = models.CharField(
        max_length=20, verbose_name='INSC EST', null=True, blank=True)
    sigla_imp = models.CharField(
        max_length=5, verbose_name='SIGLA IMP', null=True, blank=True)
    sigla_exp = models.CharField(
        max_length=5, verbose_name='SIGLA EXP', null=True, blank=True)
    serv_sigla_imp = models.CharField(
        max_length=5, verbose_name='SIGLA IMP SERV', null=True, blank=True)
    serv_sigla_exp = models.CharField(
        max_length=5, verbose_name='SIGLA EXP SERV', null=True, blank=True)
    cod_interno = models.CharField(
        max_length=20, verbose_name='COD INTERNO', null=True, blank=True)
    observacoes = models.TextField(
        verbose_name='OBSERVACOES', null=True, blank=True)

    status = models.ForeignKey(Ativo, on_delete=models.SET_NULL,
                               null=True, blank=True)

    grupo = models.ForeignKey(Grupo, related_name='grupos',
                              on_delete=models.SET_NULL,
                              null=True, blank=True)

    categoria = models.ForeignKey(Categoria, related_name='categorias',
                                  on_delete=models.SET_NULL,
                                  null=True, blank=True)

    def __str__(self):
        return self.nome
