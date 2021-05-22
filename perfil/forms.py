from django import forms
from django.contrib.auth.models import User
from .models import Perfil


class PerfilForms(forms.ModelForm):
    class Meta:
        model = Perfil
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
        fields = [
            'first_name', 'last_name', 'username',
            'password', 'password2', 'email'
        ]
    
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
        
    def clean(self):
        data = self.data
        cleaned = self.cleaned_data
        validation_msgs = {}

        username = cleaned.get('username')
        email = cleaned.get('email')
        password = cleaned.get('password')
        password2 = cleaned.get('password2')

        username_db = User.objects.filter(username=username).first()
        email_db = User.objects.filter(email=email).first()

        if self.usuario:
            if username_db:
                if self.usuario.username != username_db.username:
                    validation_msgs['username'] = 'Usuário indisponível'
            
            if email_db:
                if self.usuario.email != email_db.email:
                    validation_msgs['email'] = 'Email indisponível'
            
            if password:
                if len(password) < 6:
                    validation_msgs['password'] = 'Senha muito curta'
                
                if password != password2:
                    validation_msgs['password'] = 'Senhas precisam ser iguais'
                    validation_msgs['password2'] = 'Senhas precisam ser iguais'
        
        else:
            if username_db:
                validation_msgs['username'] = 'Usuário indisponível'
            if email_db:
                validation_msgs['email'] = 'Email indisponivel'
            
            if len(password) < 6:
                validation_msgs['password'] = 'Senha muito curta'
                
            if password != password2:
                validation_msgs['password'] = 'Senhas precisam ser iguais'
                validation_msgs['password2'] = 'Senhas precisam ser iguais'

            
        raise forms.ValidationError(validation_msgs)
        