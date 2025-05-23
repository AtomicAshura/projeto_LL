from rest_framework import serializers
import pandas as pd
from datetime import datetime
from .models import Indicador

class IndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicador
        fields = '__all__'

class PlanilhaUploadSerializer(serializers.Serializer):
    arquivo = serializers.FileField()

    def validate_arquivo(self, value):
        if not value.name.endswith(('.xlsx', '.xls')):
            raise serializers.ValidationError("Apenas arquivos Excel são aceitos")
        return value

    def create(self, validated_data):
        try:
            arquivo = validated_data['arquivo']
            df = pd.read_excel(arquivo, dtype=str, keep_default_na=False)
            
            if df.empty:
                print("DEBUG: DataFrame está vazio após a leitura do Excel!")
                raise serializers.ValidationError("Planilha vazia ou sem dados para processar.")
            
            resultados = []
            for index, row in df.iterrows():
                try:
                    # Extrai dados da linha (ajuste os índices conforme sua planilha)
                    cpf = str(row[0]).strip()
                    nome = str(row[1]).strip()
                    valor = str(row[2]).strip()
                    data_str = str(row[3]).strip()
                    
                    # Converte a data
                    data= None
                    try:
                        data = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S').date()
                    except ValueError:
                        # Se falhar, tenta o formato apenas com data (original)
                        try:
                            data = datetime.strptime(data_str, '%Y-%m-%d').date()
                        except ValueError:
                            # Tenta o formato DD/MM/YYYY
                            try:
                                data = datetime.strptime(data_str, '%d/%m/%Y').date()
                            except ValueError:
                                # Se todos falharem, levanta um erro claro
                                raise ValueError(f"Formato de data inválido: '{data_str}'")
                    
                    # Cria/atualiza o registro
                    Indicador.objects.update_or_create(
                        cpf=cpf,
                        nome=nome,
                        data_registro=data,
                        defaults={'valor': valor}
                    )
                    resultados.append(f"Linha {index+1}: OK")
                    
                except Exception as e:
                    resultados.append(f"Erro linha {index+1}: {str(e)} | Dados: {dict(row)}")
            
            return {
                "status": "success",
                "processed_rows": len(df),
                "details": resultados
            }
            
        except Exception as e:
            raise serializers.ValidationError(f"Erro ao processar planilha: {str(e)}")