import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregamento dos dados limpos
df_monthly = pd.read_parquet("outputs/tabnews_monthly_cleaned.parquet")

# Definição dos termos rastreados
termos_alvo = ['bitcoin', 'diffusion', 'claude', 'agente']

# Cálculo de Frequência Relativa
tendencias = []

for _, row in df_monthly.iterrows():
    mes = row['month_year']
    texto_mes = row['clean_text']
    
    total_palavras = len(texto_mes.split())
    
    if total_palavras > 0:
        for termo in termos_alvo:
            contagem = texto_mes.split().count(termo)
            freq_relativa = (contagem / total_palavras) * 10000
            
            tendencias.append({
                'Mês': mes,
                'Termo': termo.capitalize(),
                'Frequência (por 10k palavras)': freq_relativa
            })

df_tendencias = pd.DataFrame(tendencias)
df_tendencias['Mês'] = pd.to_datetime(df_tendencias['Mês'])

# Configuração e Exportação do Gráfico
plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid", context="paper")

ax = sns.lineplot(
    data=df_tendencias, 
    x='Mês', 
    y='Frequência (por 10k palavras)', 
    hue='Termo', 
    linewidth=2.5,
    palette=['#F7931A', '#8E44AD', '#D35400', '#2980B9']
)

plt.title('Evolução de Assuntos Tecnológicos no TabNews', fontsize=16, pad=15)
plt.xlabel('Período', fontsize=12)
plt.ylabel('Frequência Relativa', fontsize=12)
plt.legend(title='Termos Rastreados', title_fontsize='11', fontsize='10', loc='upper left')

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('outputs/tendencias_tecnologicas_tabnews.png', dpi=300)
print("Gráfico gerado e salvo como 'outputs/tendencias_tecnologicas_tabnews.png'.")
plt.show()