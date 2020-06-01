import pandas as pd
from datetime import date
import utm
import calendar
import os
from scipy.spatial.distance import squareform, pdist


nome_arquivo = "estacoes.csv"
# diretorio com arquivo 
diretorio_estacoes = 'dados'
# diretorio para salvar a matriz gerada
diretorio_resultados = 'resultados'
diretorio_distancias = 'resultados/dist_estacoes'

dados =  pd.read_csv(diretorio_estacoes+'/'+nome_arquivo, delimiter=',', decimal='.')

dados = dados[ [ 'Codigo' , 'Latitude' , 'Longitude'] ]

print('dados.size', dados.shape[0])
for i in range(dados.shape[0]):
	resultado = utm.from_latlon(dados.iloc[i].Latitude, dados.iloc[i].Longitude)
	dados.iloc[i] = [dados.iloc[i].Codigo,resultado[0],resultado[1]]
	#print(dados.iloc[i].Codigo, dados.iloc[i].Latitude, dados.iloc[i].Longitude)

dados = dados.rename(index=str, columns={"Codigo" : "Código", "Latitude": "x", "Longitude": "y"})


lista_estacoes = dados['Código'].unique()

#convertendo todos os codigos das estações de float para int
lista_estacoes = list(map(int, lista_estacoes))


dist_matrix = pd.DataFrame(squareform(pdist(dados.iloc[:, 1:]) ), columns=lista_estacoes, index=lista_estacoes )

dist_matrix.to_csv(diretorio_resultados+'/dist_matriz.csv',decimal='.')



matriz_estacoes_proximas = pd.DataFrame()
for estacao in lista_estacoes:
	estacao = int(estacao)
	#seleciona coluna da estacao alvo
	dados_selecionados = dist_matrix[estacao]
	dados_selecionados = pd.DataFrame(dados_selecionados)

	#ordenar ascendente pela coluna da estacao alvo
	dados_ordenados = dados_selecionados.sort_values(by=estacao, ascending=True)
	
	# seleciona as estações com distancia maior que 1 metro
	dados_ordenados = dados_ordenados[dados_ordenados[estacao] > 1]
	estacoes_proximas = dados_ordenados.iloc[ : , :]
	
	estacoes_proximas.to_csv(diretorio_distancias +'/'+str(estacao)+'.csv', decimal='.')
	estacoes_proximas.to_csv(diretorio_distancias+'/completo.csv', decimal='.', mode='a')





