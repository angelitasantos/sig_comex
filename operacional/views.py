from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .forms import (ImportarDadosForm)
from parceiros.models import (Parceiro, Categoria, Grupo)
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse
from io import BytesIO
import pandas as pd


class OperacionalView(TemplateView):
    template_name = 'operacional/operacional.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'OPERACIONAL'
        return context


class ImportaDadosView(TemplateView):
    template_name = 'operacional/importar_dados.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'IMPORTAR DADOS'
        return context


class ImportaParceiroView(TemplateView):
    template_name = 'operacional/importar_parceiros.html'

    def get(self, request):
        title = 'IMPORTAR PARCEIROS'
        parceiros = Parceiro.objects.all().order_by('-id')[:50]
        form = ImportarDadosForm()
        return render(request, self.template_name, {
            'title': title,
            'parceiros': parceiros,
            'form': form
        })

    def post(self, request):
        form = ImportarDadosForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo']
            df = pd.read_excel(arquivo)
            for _, row in df.iterrows():
                self.criar_parceiro(row)
            return redirect('operacional:importar_parceiros')
        msg = 'Parceiros Importados com Sucesso !'
        messages.add_message(request, constants.SUCCESS, msg)
        return render(request, self.template_name, {'form': form})

    def criar_parceiro(self, row):
        Parceiro.objects.get_or_create(
            cnpj=row['cnpj'],
            defaults={
                'nome': row['nome'],
                'razao_social': row['razao_social'],
                'insc_est': row['insc_est'],
                'sigla_imp': row['sigla_imp'],
                'sigla_exp': row['sigla_exp'],
                'serv_sigla_imp': row['serv_sigla_imp'],
                'serv_sigla_exp': row['serv_sigla_exp'],
                'cod_interno': row['cod_interno'],
                'observacoes': row['observacoes'],
                'grupo_id': row['grupo'],
                'categoria_id': row['categoria'],
                'status_id': row['status']
            }
        )


class ImportaParceiroAlteradoView(TemplateView):
    template_name = 'operacional/importar_parceiros_alterados.html'

    def get(self, request):
        title = 'IMPORTAR PARCEIROS ALTERADOS'
        parceiros = Parceiro.objects.all().order_by('-id')[:50]
        form = ImportarDadosForm()
        return render(request, self.template_name, {
            'title': title,
            'parceiros': parceiros,
            'form': form
        })

    def post(self, request):
        form = ImportarDadosForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo']
            df = pd.read_excel(arquivo)
            for _, row in df.iterrows():
                self.alterar_parceiro(row)
            return redirect('operacional:importar_parceiros_alterados')
        msg = 'Parceiros Importados com Sucesso !'
        messages.add_message(request, constants.SUCCESS, msg)
        return redirect('operacional:importar_parceiros_alterados')

    def alterar_parceiro(self, row):
        Parceiro.objects.update_or_create(
            id=row['id'],
            defaults={
                'cnpj': row['cnpj'],
                'nome': row['nome'],
                'razao_social': row['razao_social'],
                'insc_est': row['insc_est'],
                'sigla_imp': row['sigla_imp'],
                'sigla_exp': row['sigla_exp'],
                'serv_sigla_imp': row['serv_sigla_imp'],
                'serv_sigla_exp': row['serv_sigla_exp'],
                'cod_interno': row['cod_interno'],
                'observacoes': row['observacoes'],
                'grupo_id': row['grupo'],
                'categoria_id': row['categoria'],
                'status_id': row['status']
            }
        )


MODELOS_DISPONIVEIS = {
    'Parceiros': Parceiro,
    'Categorias': Categoria,
    'Grupos': Grupo,
}


class ExportaDadosView(TemplateView):
    template_name = 'operacional/exportar_dados.html'

    def get(self, request, *args, **kwargs):
        title = 'EXPORTAR DADOS'
        context = {'modelos': MODELOS_DISPONIVEIS.keys(), 'title': title}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        nome_modelo = request.POST.get('tabela')
        modelo = MODELOS_DISPONIVEIS.get(nome_modelo)

        if modelo is None:
            return HttpResponse("Modelo inválido", status=400)

        queryset = modelo.objects.all().values()
        df = pd.DataFrame(list(queryset))

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name=nome_modelo)

        buffer.seek(0)

        t = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(
            buffer,
            content_type=t
        )
        arquivo = f'attachment; filename="{nome_modelo}.xlsx"'
        response['Content-Disposition'] = arquivo
        return response
