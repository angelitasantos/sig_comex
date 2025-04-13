from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import (Ativo, Categoria, Grupo, Parceiro)
from .forms import (CategoriaForm, GrupoForm, ParceiroForm)
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Q
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)


class ParceiroView(View):
    template_name = 'parceiros/parceiros.html'

    def get(self, request):
        title = 'PARCEIROS'
        form = ParceiroForm()
        parceiros = Parceiro.objects.all().order_by('nome')
        ativos = Ativo.objects.all()
        grupos = Grupo.objects.all()
        categorias = Categoria.objects.all()

        query = request.GET.get('q', '')
        status = request.GET.get('status', '')
        grupo = request.GET.get('grupo', '')
        categoria = request.GET.get('categoria', '')

        if status:
            parceiros = parceiros.filter(status_id=status)

        if grupo:
            parceiros = parceiros.filter(grupo__id=grupo)

        if categoria:
            parceiros = parceiros.filter(categoria__id=categoria)

        default_page = 1
        page = request.GET.get('page', default_page)
        parceiros_per_page = 25

        paginator = Paginator(parceiros, parceiros_per_page)
        page_number = request.GET.get('page')
        parceiros_page = paginator.get_page(page_number)

        try:
            parceiros_page = paginator.page(page)
        except PageNotAnInteger:
            parceiros_page = paginator.page(default_page)
        except EmptyPage:
            parceiros_page = paginator.page(paginator.num_pages)

        return render(request, ParceiroView.template_name, {
            'title': title,
            'parceiros': parceiros_page,
            'categorias': categorias,
            'query': query,
            'ativos': ativos,
            'status': status,
            'grupos': grupos,
            'categoria': categoria,
            'form': form
        })

    def post(self, request):
        if request.method == 'POST':
            title = 'PARCEIROS'
            form = ParceiroForm()

            nome = request.POST.get('nome')
            razao_social = request.POST.get('razao_social')
            cnpj = request.POST.get('cnpj')
            insc_est = request.POST.get('insc_est')
            sigla_imp = request.POST.get('sigla_imp')
            sigla_exp = request.POST.get('sigla_exp')
            serv_sigla_imp = request.POST.get('serv_sigla_imp')
            serv_sigla_exp = request.POST.get('serv_sigla_exp')
            cod_interno = request.POST.get('cod_interno')
            observacoes = request.POST.get('observacoes')
            status1 = request.POST.get('status_id')
            grupo1 = request.POST.get('grupo_id')
            categoria1 = request.POST.get('categoria_id')

            status = 1 if status1 is None else status1
            grupo = 1 if grupo1 is None else grupo1
            categoria = 1 if categoria1 is None else categoria1

            if 'create' in request.POST:
                Parceiro.objects.create(
                    nome=nome,
                    razao_social=razao_social,
                    cnpj=cnpj,
                    insc_est=insc_est,
                    sigla_imp=sigla_imp,
                    sigla_exp=sigla_exp,
                    serv_sigla_imp=serv_sigla_imp,
                    serv_sigla_exp=serv_sigla_exp,
                    cod_interno=cod_interno,
                    observacoes=observacoes,
                    status_id=status,
                    grupo_id=grupo,
                    categoria_id=categoria
                )

                msg = f'Parceiro {nome} Incluído com Sucesso !'
                messages.add_message(request, constants.SUCCESS, msg)
                return redirect('parceiros:parceiros')

            elif 'update' in request.POST:
                id = request.POST.get('id')
                status = request.POST.get('status_id')
                grupo = request.POST.get('grupo_id')
                categoria = request.POST.get('categoria_id')
                parceiro = get_object_or_404(Parceiro, pk=id)

                parceiro.nome = nome
                parceiro.razao_social = razao_social
                parceiro.cnpj = cnpj
                parceiro.insc_est = insc_est
                parceiro.sigla_imp = sigla_imp
                parceiro.sigla_exp = sigla_exp
                parceiro.serv_sigla_imp = serv_sigla_imp
                parceiro.serv_sigla_exp = serv_sigla_exp
                parceiro.cod_interno = cod_interno
                parceiro.observacoes = observacoes
                parceiro.status_id = status
                parceiro.grupo_id = grupo
                parceiro.categoria_id = categoria
                parceiro.save()
                msg = f'Parceiro {nome} Alterado com Sucesso !'
                messages.add_message(request, constants.WARNING, msg)
                return redirect('parceiros:parceiros')

            elif 'search' in request.POST:
                query = request.POST.get('q', '')
                status = request.POST.get('status', '')
                grupo = request.POST.get('grupo', '')
                categoria = request.POST.get('categoria', '')

                parceiros = Parceiro.objects.all()
                ativos = Ativo.objects.all()
                grupos = Grupo.objects.all()
                categorias = Categoria.objects.all()

                if status:
                    parceiros = parceiros.filter(status__id=status)

                if grupo:
                    parceiros = parceiros.filter(grupo__id=grupo)

                if categoria:
                    parceiros = parceiros.filter(categoria__id=categoria)

                if query:
                    parceiros = parceiros.filter(
                        Q(nome__icontains=query) |
                        Q(cnpj__icontains=query) |
                        Q(sigla_imp__icontains=query) |
                        Q(sigla_exp__icontains=query) |
                        Q(serv_sigla_imp__icontains=query) |
                        Q(serv_sigla_exp__icontains=query) |
                        Q(razao_social__icontains=query)
                        )

                return render(request, ParceiroView.template_name, {
                    'title': title,
                    'parceiros': parceiros,
                    'grupo': grupo,
                    'categoria': categoria,
                    'ativos': ativos,
                    'status': status,
                    'grupos': grupos,
                    'categorias': categorias,
                    'form': form
                })

            elif 'delete' in request.POST:
                id = request.POST.get('id')
                parceiro = get_object_or_404(Parceiro, pk=id)
                # Parceiro.objects.get(id=id).delete()
                msg = f'Parceiro {parceiro.nome} Excluído com Sucesso !'
                messages.add_message(request, constants.ERROR, msg)
                return redirect('parceiros:parceiros')


class CategoriaView(View):
    template_name = 'parceiros/categorias.html'

    def get(self, request):
        title = 'CATEGORIAS'
        categorias = Categoria.objects.all().order_by('nome')
        ativos = Ativo.objects.all()
        form = CategoriaForm()

        return render(request, CategoriaView.template_name, {
            'title': title,
            'categorias': categorias,
            'ativos': ativos,
            'form': form
        })

    def post(self, request):
        if request.method == 'POST':
            if 'create' in request.POST:
                nome = request.POST.get('nome')
                status_id = 1

                Categoria.objects.create(
                    nome=nome,
                    status_id=status_id
                )

                msg = f'Categoria {nome} Incluída com Sucesso !'
                messages.add_message(request, constants.SUCCESS, msg)
                return redirect('parceiros:categorias')

            elif 'update' in request.POST:
                id = request.POST.get('id')
                nome = request.POST.get('nome')
                status_id = request.POST.get('status_id')
                categoria = get_object_or_404(Categoria, pk=id)

                categoria.nome = nome
                categoria.status_id = status_id
                categoria.save()
                msg = f'Categoria {nome} Alterada com Sucesso !'
                messages.add_message(request, constants.WARNING, msg)
                return redirect('parceiros:categorias')

            elif 'delete' in request.POST:
                id = request.POST.get('id')
                categoria = get_object_or_404(Categoria, pk=id)
                # Categoria.objects.get(id=id).delete()
                msg = f'Categoria {categoria.nome} Excluída com Sucesso !'
                messages.add_message(request, constants.ERROR, msg)
                return redirect('parceiros:categorias')


class GrupoView(View):
    template_name = 'parceiros/grupos.html'

    def get(self, request):
        title = 'GRUPOS'
        grupos = Grupo.objects.all().order_by('nome')
        ativos = Ativo.objects.all()
        form = GrupoForm()

        return render(request, GrupoView.template_name, {
            'title': title,
            'grupos': grupos,
            'ativos': ativos,
            'form': form
        })

    def post(self, request):
        if request.method == 'POST':
            if 'create' in request.POST:
                nome = request.POST.get('nome')
                status_id = 1

                Grupo.objects.create(
                    nome=nome,
                    status_id=status_id
                )

                msg = f'Grupo {nome} Incluído com Sucesso !'
                messages.success(request, msg)
                return redirect('parceiros:grupos')

            elif 'update' in request.POST:
                id = request.POST.get('id')
                nome = request.POST.get('nome')
                status_id = request.POST.get('status_id')
                grupo = get_object_or_404(Grupo, pk=id)

                grupo.nome = nome
                grupo.status_id = status_id
                grupo.save()
                msg = f'Grupo {nome} Alterado com Sucesso !'
                messages.add_message(request, constants.WARNING, msg)
                return redirect('parceiros:grupos')

            elif 'delete' in request.POST:
                id = request.POST.get('id')
                grupo = get_object_or_404(Grupo, pk=id)
                # Grupo.objects.get(id=id).delete()
                msg = f'Grupo {grupo.nome} Excluído com Sucesso !'
                messages.add_message(request, constants.ERROR, msg)
                return redirect('parceiros:grupos')
