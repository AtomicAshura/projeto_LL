from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Indicador
from login.models import Perfil
from datetime import datetime
# Create your views here.

@login_required(login_url='/login/')
def dashboard (request):
    user= request.user
    perfil= Perfil.objects.get(user=user)
    cpf_usuario= perfil.cpf

    indicadores= Indicador.objects.filter(cpf=cpf_usuario)

    start_date= request.GET.get('start_date')
    end_date= request.GET.get('end_date')

    if start_date:
        indicadores= indicadores.filter(data_registro__gte= start_date)
    if end_date:
        indicadores = indicadores.filter(data_registro__lte=end_date)

    return  render(request, 'dashboard.html', {
        'indicadores':indicadores,
        'start_date': start_date,
        'end_date':end_date
        })
