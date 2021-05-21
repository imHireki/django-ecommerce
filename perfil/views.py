from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms
from .models import Perfil
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = Perfil.objects.filter(
                usuario=self.request.user
            ).first()

            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    instance=self.request.user,
                    usuario=self.request.user,
        
                ),
                'perfilform': forms.PerfilForms(
                    data=self.request.POST or None,
                    instance=self.perfil,
                )
            }
        else: 
            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                ),
                'perfilform': forms.PerfilForms(
                    data=self.request.POST or None,
                    instance=self.perfil
                )
            }

        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']

        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )

    def get(self, *args, **kwargs):
        return self.renderizar
    

class CriarAtualizar(BasePerfil):
    def post(self, *args, **kwargs):
        username = self.userform.cleaned_data['username']
        password = self.userform.cleaned_data['password']
        email = self.userform.cleaned_data['email']
        first_name = self.userform.cleaned_data['first_name']
        last_name = self.userform.cleaned_data['last_name']
        
        if self.request.user.is_authenticated:
            usuario = User.objects.filter(username=username).first()

            usuario.username = username
            usuario.set_password(password)
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name

            usuario.save()
            
            if not self.perfil:
                self.perfilform.cleaned_data['usuario'] = usuario
                perfil = Perfil(**self.perfilform.cleaned_data)
                perfil.save()
            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save() 

        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            self.perfilform.cleaned_data['usuario'] = usuario
            perfil = Perfil(**self.perfilform.cleaned_data)
            perfil.save() 
            
        # if password:
        authenticate(
            self.request, 
            username=username, password=password 
        )
        if authenticate:
            login(self.request, user=usuario)
        
        return self.renderizar
