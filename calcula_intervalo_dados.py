import math
import pandas as pd
from datetime import date
import datetime
import calendar
import os
from scipy.spatial.distance import squareform, pdist

#nome do arquivo que contem a matriz de chuva que se deseja preencher
nome_arquivo = "matriz_vazao_completa.csv"
# diretorio onde a matriz do item anterior está salva
diretorio_entradas = 'resultados'
# diretorio para salvar a matriz preenchida
diretorio_resultados = 'resultados'


dados =  pd.read_csv(diretorio_entradas+'/'+nome_arquivo, delimiter=',', decimal='.')
#dados = dados.sort_values(by='data', ascending=True)

#print(dados)
print('\nSTART -> ', pd.to_datetime(dados.iloc[0]['data'], format='%Y-%m-%d', errors='ignore'))
dates_quant = 0
for i in range(dados.shape[0]-1):
	dates_quant += 1
	actual_date = pd.to_datetime(dados.iloc[i]['data'], format='%Y-%m-%d', errors='ignore')
	predict_date = actual_date + datetime.timedelta(days=1)
	next_date = pd.to_datetime(dados.iloc[i+1]['data'], format='%Y-%m-%d', errors='ignore')

	if(predict_date != next_date):
		print('END -> ', actual_date, 'Dias : ', dates_quant)
		print('\nSTART -> ', next_date)
		dates_quant = 0

print('END -> ', pd.to_datetime(dados.iloc[dados.shape[0]-1]['data'], format='%Y-%m-%d', errors='ignore'))


	#print(i,' : ', actual_date, ' : ', predict_date, ' : ', (predict_date ==  next_date))
