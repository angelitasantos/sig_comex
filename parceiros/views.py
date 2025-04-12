from django.shortcuts import render
from django.views import View


class ParceiroView(View):
    template_name = 'parceiros/parceiros.html'

    def get(self, request):
        title = 'PARCEIROS'
        return render(request, ParceiroView.template_name, {
            'title': title
        })
