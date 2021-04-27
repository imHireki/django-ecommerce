from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . import models

class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
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
        error_msgs_validation = {}
        
        username = cleaned.get('username')
        email = cleaned.get('email')
        password = cleaned.get('password')
        password2 = cleaned.get('password2')
        
        usuario_db = User.objects.filter(username=username).first()
        email_db = User.objects.filter(email=email).first()
        
        if self.usuario:
            
            if usuario_db:
                if self.usuario.username != usuario_db.username:
                    error_msgs_validation['username'] = 'a'

        if error_msgs_validation:
            raise ValidationError(error_msgs_validation)
