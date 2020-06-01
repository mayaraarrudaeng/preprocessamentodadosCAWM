import math
import numpy as np
import pandas as pd
import os

#nome do arquivo que contem os dados de chuva
arquivo_chuvas = "matriz_chuva_completa.csv"
#nome do arquivo que contém as areas
arquivo_areas = "areas.csv"
# diretorio onde os arquivos de chuva e matriz estão salvos
diretorio_entradas = 'dados'
# diretorio para salvar a chuva media
diretorio_resultados = 'resultados'


dados_chuvas = pd.read_csv(diretorio_entradas+'/'+arquivo_chuvas, delimiter=',', decimal='.')
dados_areas = pd.read_csv(diretorio_entradas+'/'+arquivo_areas, delimiter=',', decimal='.')
chuvas_areas = dados_chuvas

#alterar o nome da primeira coluna
chuvas_areas.columns.values[0] = 'Data'
#definindo a coluna data como índice
chuvas_areas.set_index('Data', inplace=True)

print(chuvas_areas)
	
print(range(chuvas_areas.shape[0]))
print(range(dados_areas.shape[0]))


dados_areas = dados_areas[ ['Codigo','Area'] ]
chuvas_areas['chuva_media'] = " "
print(chuvas_areas)
for i in range(chuvas_areas.shape[0]):
	area_total = 0.0
	chuva = 0.0
	print(i)
	for j in range(dados_areas.shape[0]):
		#codigo = str(int(dados_areas.iloc[j]['Codigo']))
		if np.isnan(chuvas_areas.iloc[i,j]) == True:
			pass
		else:
			area = float(dados_areas.iloc[j]['Area'])
			area_total += area
			#print(codigo, area)
			chuva += chuvas_areas.iloc[i,j] * area

	if area_total == 0.0:
		area_total=1.0
	chuvas_areas.iloc[i,dados_areas.shape[0]] = chuva/area_total
'''for i in range(chuvas_areas.shape[0]):
	area_total = 0.0
	chuva = 0.0
	print(i)
	for j in range(dados_areas.shape[0]):
		#codigo = str(int(dados_areas.iloc[j]['Codigo']))
		if np.isnan(chuvas_areas.iloc[i,j]) == True:
			pass
		else:
			area = float(dados_areas.iloc[j]['Area'])
			area_total += area
			#print(codigo, area)
			chuva += chuvas_areas.iloc[i,j] * area

	print(area_total)
	if area_total == 0.0:
		area_total=1.0
	chuvas_areas.iloc[i,dados_areas.shape[0]] = chuva/area_total'''


'''for i in range(dados_areas.shape[0]):
	codigo = str(int(dados_areas.iloc[i]['Codigo']))
	if np.isnan(chuvas_areas.loc[:,codigo]) == True:
		pass
	else:
		area = float(dados_areas.iloc[i]['Area'])
		area_total += area
		print(codigo, area)
		chuvas_areas.loc[:,codigo] *= area'''

#print("Area Total: ", area_total)



#chuvas_areas.loc[:,'chuva_media'] /= area_total


#print(chuvas_areas)

chuvas_areas.to_csv(diretorio_resultados+'/precipitacao_media2.csv', decimal='.', index=True)

