from django.views.generic import View
from django.shortcuts import render
from . import forms 

class BasePerfil(View):
    template_name = 'perfil/criar.html'
    
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'userform': forms.UserForm(
                # send data to forms
                data=self.request.POST or None,
                # populate forms
                instance=self.request.user,
                # send usuario to forms
                usuario=self.request.user
            ) 
        }

        self.renderizar = render(
            self.request, self.template_name, self.contexto
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
