from django.http import HttpResponse
from django.views.generic import View


class Pagar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagar')


class FecharPedido(View):
    pass


class Detalhe(View):
    pass
