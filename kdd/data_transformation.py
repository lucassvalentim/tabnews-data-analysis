import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

df = pd.read_parquet("data/tabnews_data.parquet")

# Filtrar o  nó 'NewsletterOficial' (possível bot) para evitar viés humano
df_filtered = df[df['owner_username'] != 'NewsletterOficial'].copy()

print(f"Registros após remoção do bot oficial: {df_filtered.shape[0]}")

print("Extraindo novos atributos numéricos a partir do texto e datas...")

df_filtered['title_length'] = df_filtered['title'].str.len()
df_filtered['body_length'] = df_filtered['body'].str.len()

df_filtered['has_source_url'] = df_filtered['source_url'].notna().astype(int)

df_filtered['published_at'] = pd.to_datetime(df_filtered['published_at'])
df_filtered['published_hour'] = df_filtered['published_at'].dt.hour

# Seleciona apenas os atributos estruturais numéricos que fazem sentido para o algoritmo
atributos_para_mineracao = [
    'title_length', 'body_length', 'has_source_url', 'published_hour',
    'tabcoins', 'tabcoins_credit', 'tabcoins_debit', 'children_deep_count'
]

df_selected = df_filtered[atributos_para_mineracao].copy()

print("Aplicando Normalização (MinMax Scaling)...")
scaler = MinMaxScaler()

df_normalized = pd.DataFrame(
    scaler.fit_transform(df_selected), 
    columns=df_selected.columns,
    index=df_selected.index
)

print("\n--- Primeiras 5 linhas do Dataset Pronto e Normalizado ---")
print(df_normalized.head())

# Salvar o dataset transformado para usar na etapa de Mineração
df_normalized.to_parquet("data/tabnews_transformed.parquet")
print("\nDataset transformado salvo com sucesso em 'data/tabnews_transformed.parquet'")