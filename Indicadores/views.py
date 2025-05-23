from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Indicador
from login.models import Perfil
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .serializers import IndicadorSerializer, PlanilhaUploadSerializer
import pandas as pd
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

class IndicadorAPI (APIView):
    def get (self, request):
        cpf = request.GET.get('cpf')
        start_date= request.GET.get ('start_date')
        end_date= request.GET.get('end_date')
        
        indicadores= Indicador.objects.all()

        if cpf:
            indicadores= indicadores.filter(cpf=cpf)
        if start_date:
            indicadores= indicadores.filter(data_registro__gte = start_date)
        if end_date:
            indicadore= indicadores.filter(data_registro__lte=end_date)
        
        serializer= IndicadorSerializer (indicadores, many= True)
        return Response (serializer.data)
    def post (self, request):
        serializer= IndicadorSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensagem':'Indicador criado com sucesso'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UploadPlanilhaAPI(APIView):
    parser_classes = (MultiPartParser,)
    
    def post(self, request, format=None):
        serializer = PlanilhaUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = serializer.save()
                return Response({
                    "status": "success",
                    "message": f"Processadas {result['processed_rows']} linhas",
                    "details": result['details']
                }, status=200)
            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e),
                    "details": []
                }, status=400)
        
        return Response({
            "status": "error",
            "message": serializer.errors,
            "details": result
        }, status=400)