import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_parquet("data/tabnews_data.parquet")

# Filtrar o bot institucional para manter o comportamento orgânico humano
df_filtered = df[df['owner_username'] != 'NewsletterOficial'].copy()

# Engenharia de Atributos
df_filtered['title_length'] = df_filtered['title'].str.len()
df_filtered['body_length'] = df_filtered['body'].str.len()
df_filtered['has_source_url'] = df_filtered['source_url'].notna().astype(int)
df_filtered['published_hour'] = pd.to_datetime(df_filtered['published_at']).dt.hour

# Definição da Classe Alvo (Target) baseada na mediana empírica: é popular de med > 2
mediana_corte = 2
df_filtered['is_popular'] = (df_filtered['tabcoins'] > mediana_corte).astype(int)

# Verificar o equilíbrio das classes
print("--- Distribuição da Classe Alvo (is_popular) ---")
print(df_filtered['is_popular'].value_counts(normalize=True))
print(df_filtered['is_popular'].value_counts())
print("-" * 50)

X = df_filtered[['title_length', 'body_length', 'has_source_url', 'published_hour']]
y = df_filtered['is_popular']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

modelo_arvore = DecisionTreeClassifier(max_depth=5, random_state=42, criterion='gini')
modelo_arvore.fit(X_train, y_train)

y_pred = modelo_arvore.predict(X_test)

print("\n=== MATRIZ DE CONFUSÃO ===")
print(confusion_matrix(y_test, y_pred))

print("\n=== RELATÓRIO DE CLASSIFICAÇÃO ===")
print(classification_report(y_test, y_pred, target_names=['Não Popular (0)', 'Popular (1)']))

print(f"Acurácia Geral do Modelo: {accuracy_score(y_test, y_pred):.4f}")
print("-" * 50)

# Extração da Importância dos Atributos
importancias = pd.Series(modelo_arvore.feature_importances_, index=X.columns).sort_values(ascending=False)

print("\n=== IMPORTÂNCIA DOS ATRIBUTOS PARA A POPULARIDADE ===")
print(importancias)

# Plotagem Gráfica da Importância das Variáveis
plt.figure(figsize=(10, 5))
sns.set_theme(style="whitegrid", context="paper")
sns.barplot(x=importancias.values, y=importancias.index, palette="viridis")
plt.title("Importância dos Atributos na Predição de Popularidade (TabNews)")
plt.xlabel("Grau de Importância (Gini Importance)")
plt.ylabel("Atributos Estruturais")
plt.tight_layout()
plt.show()