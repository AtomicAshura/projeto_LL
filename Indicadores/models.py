from django.db import models
import datetime
# Create your models here.

class Indicador (models.Model):
    nome= models.CharField(max_length=100)
    valor = models.FloatField()
    data_registro = models.DateField(default=datetime.date.today)
    cpf= models.CharField(max_length=14)

    def __str__(self):
        return f"{self.nome} - {self.cpf}"