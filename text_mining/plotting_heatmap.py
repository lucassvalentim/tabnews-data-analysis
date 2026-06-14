import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados limpos
df_monthly = pd.read_parquet("outputs/tabnews_monthly_cleaned.parquet")

# Definir uma lista maior e mais rica de termos (Família IA + Linguagens + Carreira)
# Você pode trocar essas palavras pelo que achar melhor!
termos_mapa = [
    'bitcoin', 'cripto', 'layoff', 'júnior', 'carreira', 
    'react', 'python', 'rust', 'docker', 'neovim',
    'chatgpt', 'claude', 'gemini', 'deepseek', 'agente'
]

# Construir a Matriz de Frequências
dados_matriz = []

for _, row in df_monthly.iterrows():
    mes = row['month_year']
    texto_mes = row['clean_text']
    total_palavras = len(texto_mes.split())
    
    if total_palavras > 0:
        linha_mes = {'Mês': mes}
        for termo in termos_mapa:
            contagem = texto_mes.split().count(termo)
            # Frequência relativa (por 10k palavras)
            freq_relativa = (contagem / total_palavras) * 10000
            linha_mes[termo.capitalize()] = freq_relativa
        dados_matriz.append(linha_mes)

# Converter para DataFrame e ajustar o índice para o Heatmap
df_heatmap = pd.DataFrame(dados_matriz)
df_heatmap['Mês'] = pd.to_datetime(df_heatmap['Mês']).dt.strftime('%Y-%m') # Formato mais limpo
df_heatmap.set_index('Mês', inplace=True)

# Transpor a matriz (Meses no eixo X, Palavras no eixo Y)
df_heatmap_t = df_heatmap.T

# Plotagem do Mapa de Calor
plt.figure(figsize=(16, 8))
sns.set_theme(style="white", context="paper")

# Plotando com a paleta 'YlGnBu' (Yellow to Green to Blue) ou 'flare'
ax = sns.heatmap(
    df_heatmap_t, 
    cmap="YlGnBu", 
    linewidths=.5, 
    cbar_kws={'label': 'Frequência Relativa (Intensidade)'}
)

plt.title('Mapa de Calor: Intensidade de Assuntos no TabNews (2022 - 2026)', fontsize=16, pad=20)
plt.xlabel('Período (Ano-Mês)', fontsize=12)
plt.ylabel('Termos Rastreados', fontsize=12)

# Rotacionar os rótulos do eixo X para não encavalarem
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0, fontweight='bold')
plt.tight_layout()

# Salvar para o PDF
plt.savefig('outputs/heatmap_tendencias_tabnews.png', dpi=300)
print("Gráfico de calor gerado e salvo como 'outputs/heatmap_tendencias_tabnews.png'.")
plt.show()