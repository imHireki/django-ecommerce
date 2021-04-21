from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação senha'
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'password',
            'password2', 'email'
        )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # received from context
        self.usuario = usuario
    
    def clean(self, *args, **kwargs):
        # received from context
        data = self.data
        
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')

        # query db to see if the usuario_data is on db
        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As duas senhas não conferem'
        error_msg_password_short = 'Sua senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório'

        #  user logged in
        if self.usuario:

            # error if a logged user is trying to define a username that already is on db
            if usuario_db: # if any profile exists with the sent username
                if self.usuario.username != usuario_db.username: # if logged username != queried username
                    validation_error_msgs['username'] =  error_msg_user_exists

            # error if a logged user is trying to define a email that already is on db
            if email_db: # if any profile exists with the sent username
                if self.usuario.email != email_db.email: # if logged user's email != queried email
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match
            
                if len(password_data) < 6:
                    validation_error_msgs['password'] =  error_msg_password_short

        # user not logged in
        else:
            pass
        
        # it raises all error msgs at once
        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))

