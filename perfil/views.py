from django.http import HttpResponse
from django.views.generic import View


class Criar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Criar')


class Atualizar(View):
    pass


class Login(View):
    pass


class Logout(View):
    pass
