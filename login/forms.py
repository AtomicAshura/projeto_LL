from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class CadastroForm(forms.ModelForm):
    username= forms.CharField(label='Usuário', widget=forms.TextInput(attrs={'placeholder':'Usuário'}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Senha'}), label='Senha',)
    cpf= forms.CharField(label= 'CPF', widget=forms.TextInput(attrs={'placeholder':'CPF'}))

    class Meta:
        model= User
        fields= ['username','password']

    def save(self, commit= True):
        user= super().save(commit=True)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Perfil.objects.create(user=user, cpf=self.cleaned_data['cpf'])
        return user
    