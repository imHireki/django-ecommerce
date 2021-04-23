from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . import models


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        field = '__all__'
        exclude = ('usuario', )


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )
    
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação Senha'
    )
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username',
            'password', 'password2', 'email'
        )
    
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
    
    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}
        
        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password = cleaned.get('password')
        password2 = cleaned.get('password2')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()
        
        if self.usuario:
            if usuario_db:
                if self.usuario.username != usuario_db.username:
                    validation_error_msgs['username'] = 'usuário já existe'
            
            if email_db:
                if self.usuario.email != email_db.email:
                    validation_error_msgs['email'] = 'email já existe'
            
            if password:
                if password != password2:
                    validation_error_msgs['password'] = 'senhas não correspondem'
                    validation_error_msgs['password2'] = 'senhas não correspondem'

                if len(password) < 6:
                    validation_error_msgs['password'] = 'Senha curta'
        else:
            pass

        if validation_error_msgs:
            raise ValidationError(validation_error_msgs)
