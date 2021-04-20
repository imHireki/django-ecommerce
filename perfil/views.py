from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render
from . import forms


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().seteup(*args, **kwargs)

        if self.request.user.is_authenticated:
            self.context = {
                'userform': forms.Userform(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                )
            }
        else:
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                )
            }

        self.renderizar = render(
            self.request, self.template_name, self.context
        )

    def get(self, *args, **kwargs):
        return self.renderizar
    

class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        return self.renderizar


class Atualizar(View):
    pass


class Login(View):
    pass


class Logout(View):
    pass
