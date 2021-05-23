from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms
from .models import Perfil
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from copy import deepcopy
from django.contrib import messages


class Logout(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request, 
                'Usuário precisa estar logado para fazer logout'
            )
            return redirect('perfil:criar')
        
        carrinho = deepcopy(
            self.request.session.get('carrinho'), {}
        )

        logout(self.request)
        self.request.session['carrinho'] = carrinho

        return redirect('produto:lista')
        
class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.warning(
                self.request,
                'Usuário ou senha inválidos'

            )
            return redirect('perfil:criar')
        
        login_user = authenticate(
            self.request,
            username=username,
            password=password
        )

        if not login_user:
            messages.warning(
                self.request,
                'Usuário ou senha Inválidos'
            )
        
        if login_user:
            login(
                self.request,
                login_user
            )

        return redirect('perfil:criar')

    

class BasePerfil(View):
    template_name = 'perfil/atualizar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = deepcopy(self.request.session.get('carrinho'), {})

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
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(
                self.request, 
                'O formulário contém dados inválidos'
            )
            return redirect('perfil:criar')
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')
        
        if self.request.user.is_authenticated:
            usuario = User.objects.filter(username=self.request.user).first()

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
        
        messages.success(
            self.request,
            'Alterações Salvas!'
        )
        # if password:
        authentic = authenticate(
            self.request, 
            username=username, password=password 
        )
        if authentic:
            login(self.request, user=usuario)

        self.request.session['carrinho'] = self.carrinho    
        self.request.session.save()

        return redirect('perfil:criar')
