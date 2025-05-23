from django.db import models
import datetime
from django.core.validators import MinLengthValidator
# Create your models here.

class Indicador (models.Model):
    nome= models.CharField(max_length=100)
    valor = models.FloatField()
    data_registro = models.DateField(default=datetime.date.today)
    cpf= models.CharField(max_length=14)

    class Meta:
        unique_together = ('cpf', 'nome', 'data_registro')
        
    def __str__(self):
        return f"{self.nome} - {self.cpf}"