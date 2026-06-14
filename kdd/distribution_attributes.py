import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_parquet("../data/tabnews_data.parquet")

sns.set_theme(style="whitegrid", context="paper")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 13})

# Histograma de TabCoins
sns.histplot(data=df, x='tabcoins', bins=60, ax=axes[0, 0], color='#4C72B0', alpha=0.8)
axes[0, 0].set_yscale('log')
axes[0, 0].set_title('Distribuição de TabCoins (Frequência em Escala Log)')
axes[0, 0].set_xlabel('Saldo de TabCoins')
axes[0, 0].set_ylabel('Quantidade de Posts (Log)')

# Boxplot de TabCoins
sns.boxplot(data=df, x='tabcoins', ax=axes[0, 1], color='#4C72B0', width=0.4)
axes[0, 1].set_title('Dispersão e Outliers de TabCoins')
axes[0, 1].set_xlabel('Saldo de TabCoins')

# Histograma de Comentários
sns.histplot(data=df, x='children_deep_count', bins=60, ax=axes[1, 0], color='#DD8452', alpha=0.8)
axes[1, 0].set_yscale('log')
axes[1, 0].set_title('Distribuição de Comentários (Frequência em Escala Log)')
axes[1, 0].set_xlabel('Quantidade de Respostas (Deep Count)')
axes[1, 0].set_ylabel('Quantidade de Posts (Log)')

# Boxplot de Comentários
sns.boxplot(data=df, x='children_deep_count', ax=axes[1, 1], color='#DD8452', width=0.4)
axes[1, 1].set_title('Dispersão e Outliers de Comentários')
axes[1, 1].set_xlabel('Quantidade de Respostas')

plt.tight_layout()
plt.savefig('outputs/distribution_attributes.png')
plt.show()