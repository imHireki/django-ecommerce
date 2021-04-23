from django.views.generic import View
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from . import forms 
import copy


class BasePerfil(View):
    template_name = 'perfil/criar.html'
    
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(
            self.request.session.get('carrinho'), {}
        )
        
        self.contexto = {
            'userform': forms.UserForm(
                data=self.request.POST or None,
                instance=self.request.user,
                usuario=self.request.user
            ),
        }

        self.userform = self.contexto['userform']
        
        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        
        if not self.userform.is_valid():
            messages.error(
                self.request, 'algo de errado não está certo'
            )
            return self.renderizar

        username = self.userform.cleaned_data.get('username')
        email = self.userform.cleaned_data.get('email')
        password = self.userform.cleaned_data.get('password')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # update
        if self.request.user.is_authenticated:

            usuario = User.objects.filter( # get object or 404
                username=self.request.user.username
            ).first()
            
            usuario.username = username
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            if password:
                usuario.set_password(password)

            usuario.save()

        # create 
        else:
            pass

        if password:
            autentica = authenticate(
                username=username,
                password=password
            )

            if autentica:
                login(self.request, usuario)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        return self.renderizar


class Atualizar(View):
    pass


class Login(View):
    pass


class Logout(View):
    pass
