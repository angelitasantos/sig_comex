from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.messages import constants


class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        title = 'NOME EMPRESA'
        messages.add_message(
                request, constants.SUCCESS, 'Mensagem Funcionando!')
        return render(request, HomeTemplateView.template_name, {
            'title': title
        })
