from django.views.generic import View
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from . import forms, models
import copy


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        
        self.carrinho = copy.deepcopy(
            self.request.session.get('carrinho'), {}
        )
        
        self.perfil = None
        
        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'
            
            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user
            ).first()
            
            self.contexto = {
                'userform': forms.UserForm(
                    usuario=self.request.user,
                    instance=self.request.user,
                    data=self.request.POST or None,
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                )
            }
        
        else:
            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                )
            }

        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']
        
        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            pass
        
        username = self.userform.cleaned_data.get('username')
        email = self.userform.cleaned_data.get('email')
        password = self.userform.cleaned_data.get('password')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')
        
        if self.request.user.is_authenticated:

            usuario = User.objects.filter(username=username).first()
            usuario.username = username
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            if password:
                usuario.set_password(password)
            usuario.save()

            if self.perfil:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()
            else:
                self.perfilform.cleaned_data['usuario'] = usuario
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                perfil.save()

        else:
            usuario = self.userform.save()
            usuario.set_password(password)
            usuario.save()
        
        autentica = authenticate(
            username=usuario.username,
            password=password
        )
        if autentica:
            login(self.request, user=usuario)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        return self.renderizar

class Atualizar(View):
    pass


class Login(View):
    pass


class Logout(View):
    pass
