import pandas as pd

df = pd.read_parquet("data/tabnews_data.parquet")

# Verifica as dimensões da base utilizada
print("----- Dimensões do Dataset ------")
print(f"Total de registros (posts): {df.shape[0]}")
print(f"Total de atributos (colunas): {df.shape[1]}\n")

# Analisar tipos de dados e identificação inicial de nulos
print("----- Informações estruturais do Dataframe -----")
print(df.info())
print("\n")

# Extrair Estatísticas Básicas dos atributos quantitativos (mín, máx, média, mediana e desvio-padrão)
print("--- Estatísticas Básicas dos Atributos Numéricos ---")
atributos_numericos = ['tabcoins', 'tabcoins_credit', 'tabcoins_debit', 'children_deep_count']

estatisticas = df[atributos_numericos].describe().T
estatisticas['median'] = df[atributos_numericos].median()

estatisticas = estatisticas[['min', 'max', 'mean', 'median', 'std']]

print(estatisticas.to_string())

print("\n--- Top 5 Usuários com Maior Volume de Publicações ---")
print(df['owner_username'].value_counts().head(5))