import math
import pandas as pd
from datetime import date
import calendar
import os
from scipy.spatial.distance import squareform, pdist

#nome do arquivo que contem a matriz de chuva que se deseja preencher
nome_arquivo = "matriz_chuva_completa.csv"
# diretorio onde a matriz do item anterior está salva
diretorio_entradas = 'resultados'
# diretorio para salvar a matriz preenchida
diretorio_resultados = 'resultados'
#diretório da pasta que contem as distancias entre pares de estações
diretorio_estacoes_proximas = 'resultados/dist_estacoes'


dados =  pd.read_csv(diretorio_entradas+'/'+nome_arquivo, delimiter=',', decimal='.')
dadosOriginais =  pd.read_csv(diretorio_entradas+'/'+nome_arquivo, delimiter=',', decimal='.')

#dados.iloc[i] -para cada linha imprime todas as colunas

estacoes = dados.iloc[ : , 1: ].columns
#print(estacoes)

precip_media_anual = {} #precipitação média anual
#calculo da precipitação média anual
for estacao in estacoes:
	precip_media_anual[str(estacao)] = dados[estacao].mean(skipna=True)*365.25
#print(precip_media_anual)



for i in range(dados.shape[0]):
	for estacao in estacoes:
		#print( math.isnan( dados.iloc[i][estacao]) )
		if( math.isnan( dadosOriginais.iloc[i][estacao]) ):
			#print('Linha ', i, 'estacao ', estacao,' eh VAZIA.')
			est_proximas = pd.read_csv(diretorio_estacoes_proximas+'/'+estacao+'.csv', delimiter=',', decimal='.')
			est_proximas = est_proximas.iloc[: , :1].values
			#print(est_proximas)
			tres_vizinhos = []
			
			for j in range(3):
				if(math.isnan(dadosOriginais.iloc[i][ str(est_proximas[j][0]) ]) == False):
					tres_vizinhos.append(str(est_proximas[j][0]))
				
			#print(tres_vizinhos)
			if(len(tres_vizinhos) < 1):
				#print('Não há vizinhos suficientes para a estimativa!')
				continue;
			preci_d_vizinhos = {}
			
			for vizinho in tres_vizinhos:
				preci_d_vizinhos[vizinho] = (dadosOriginais.iloc[i][vizinho])
			
			#print(preci_d_vizinhos)

			valor_estimado = 0
			for vizinho in tres_vizinhos:
				valor_estimado += (preci_d_vizinhos[vizinho] /precip_media_anual[vizinho])
			
			#valor_estimado = ((preci_d_vizinhos[tres_vizinhos[0]] /precip_media_anual[tres_vizinhos[0]]) + (preci_d_vizinhos[tres_vizinhos[1]] /precip_media_anual[tres_vizinhos[1]]) + (preci_d_vizinhos[tres_vizinhos[2]] /precip_media_anual[tres_vizinhos[2]]))
			
			valor_estimado = valor_estimado*precip_media_anual[estacao]
			valor_estimado /= len(tres_vizinhos)

			#print(valor_estimado)
			dados.at[i, estacao] = valor_estimado
			#soma_precitacao_vizinhos = dados.iloc[i][ tres_vizinhos[0] ] + dados.iloc[i][tres_vizinhos[1]] + dados.iloc[i][ tres_vizinhos[2] ]
				

	

dados.to_csv(diretorio_resultados+'/matriz_preenchida.csv', decimal='.', index=False)

matriz_validos = dados.dropna()
matriz_validos.columns.values[0] = 'data'
matriz_validos.to_csv(diretorio_resultados+'/matriz_preenchida_validos.csv', decimal = '.', index = False)

dados[dados.isnull().any(axis=1)].to_csv(diretorio_resultados+'/matriz_preenchida_invalidos.csv', decimal='.', index=False)






