import pandas as pd
from datetime import date
import calendar
import os, fnmatch


def construcao_matriz():

	# diretorio com os arquivos CSV das estações
	diretorio_estacoes = path
	# diretorio para salvar a matriz gerada
	diretorio_resultados = path

	lista_arquivos = os.listdir(diretorio_estacoes)

	print(lista_arquivos)

	# matriz final Indices: datas; Colunas: códigos das estações; Valores: quantidade de chuva 
	matriz_completa = pd.DataFrame()

	# para cada arquivo insere os dados de chuva na matriz completa
	extensao = "*.csv"  
	for arquivo in lista_arquivos:
		if fnmatch.fnmatch(arquivo, extensao):
			print('Arquivo : ', arquivo)

			#skiprows é um parâmetro utilizado para ignorar linhas de um csv, nesse caso, estaos ignorando as 11 primeiras linhas do arquivo
			dados = pd.read_csv(diretorio_estacoes+'/'+arquivo, delimiter=';', decimal=',',index_col=False, skiprows = 11)
			if(dados.size == 0):
				continue

			cod_estacao = dados['EstacaoCodigo'].iloc[0]
			
			# seleciona as colunas de chuva
			# pegar todas as linhas das colunas definidas (colunas 13 a 44)
			dadosChuvas  = dados.iloc[: , 13:44] 
			# seleciona as colunas de data
			datas = dados['Data']
			# uniao das colunas de datas e chuvas
			dados = pd.concat([datas , dadosChuvas],axis=1,sort=True)

			nLinhas = dados.shape[0] # numero de meses, um para cada linha


			matriz = pd.DataFrame(columns=[cod_estacao])

			# para cada mês é selcionado o registro de chuva para cada dia
			for indice in range(nLinhas):

				day, month, year = map(int, dados.values[indice][0].split('/'))
				# monthsize quantidade de dias do mês selecionado
				weekday , monthsize = calendar.monthrange(year,month)
							
				for dia in range(day,monthsize+1):
					data = date(year,month, dia)
					matriz.loc[data] = dados.iloc[indice].values[dia]

		matriz.index.name = 'data'

		# concatena as matrizes
		matriz_completa = pd.concat([matriz_completa , matriz],axis=1, sort=True)


	#dá nome para a coluna que representa o índice (no caso a coluna de datas)
	matriz_completa.index.name = 'data'

	#print (matriz_completa)

	#pega o primeiro valor do índice (no caso, a primeira data)
	dia_inicio = matriz_completa.index[0]

	#pega o último valor do índice (no caso, a última data)
	dia_fim = matriz_completa.index[-1]

	#pega apenas a coluna 'data' do arquivo que se deseja univormizar e converte o tipo para datetime
	matriz_completa.index = pd.to_datetime(matriz_completa.index)

	#cria um intervalo de tempo 
	datelist = pd.date_range(start = dia_inicio, end = dia_fim)

	#transforma o datalist em um dataframe
	inter_datas = pd.DataFrame(data = datelist, columns = ['data'])

	#uniformiza a matriz de dados (dias corridos)
	matriz_completa_uni = pd.merge(inter_datas,matriz_completa, how = 'left', left_on = 'data', right_index=True)

	matriz_completa_uni.to_csv(diretorio_resultados+'/matriz_chuva_completa.csv',index= False)

	#transforma a coluna data em índice
	matriz_completa_uni.set_index('data', inplace = True)

	matriz_completa_uni.to_csv(diretorio_resultados+'/matriz_chuva.csv')


	return		