import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# Configuração de Stopwords
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('portuguese'))
stop_words.update([
    'como', 'sobre', 'aqui', 'pra', 'fazer', 'pode', 'alguém', 'ter', 
    'vai', 'acho', 'tudo', 'porque', 'então', 'bem', 'ser',
    'nbsp', 'strong', 'span', 'blank', 'font', 'details', 'summary', 
    'margin', 'paragraph', 'block', 'heading', 'vertical', 'border', 
    'const', 'var', 'int', 'struct', 'none', 'null', 'true', 'false'
])

# Carrega dados
df = pd.read_parquet("../data/tabnews_transformed.parquet")
df['full_text'] = df['title'].fillna('') + " " + df['body'].fillna('')

def clean_text(text):
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-zA-ZáéíóúâêôãõçÁÉÍÓÚÂÊÔÃÕÇ]', ' ', text)
    
    words = text.lower().split()
    words = [w for w in words if w not in stop_words and len(w) > 2]
    return " ".join(words)

print("Iniciando limpeza do texto...")
df['clean_text'] = df['full_text'].apply(clean_text)

# Agrupamento Temporal
df['published_at'] = pd.to_datetime(df['published_at'])
df['month_year'] = df['published_at'].dt.to_period('M')

df_monthly = df.groupby('month_year')['clean_text'].apply(lambda x: ' '.join(x)).reset_index()
df_monthly['month_year'] = df_monthly['month_year'].astype(str)

# Extração TF-IDF
print("Aplicando TF-IDF e extraindo top termos...")
tfidf_vectorizer = TfidfVectorizer(max_df=0.85, min_df=2, max_features=1000)
tfidf_matrix = tfidf_vectorizer.fit_transform(df_monthly['clean_text'])
feature_names = tfidf_vectorizer.get_feature_names_out()

# Formatação dos Resultados
dados_tabela = []
for i, month in enumerate(df_monthly['month_year']):
    row_data = tfidf_matrix.getrow(i).todense().tolist()[0]
    word_scores = [(feature_names[idx], score) for idx, score in enumerate(row_data)]
    word_scores = sorted(word_scores, key=lambda x: x[1], reverse=True)
    
    top_5_words = [word for word, score in word_scores[:5]]
    dados_tabela.append({
        'Mes_Ano': month,
        'Top_Termos': ', '.join(top_5_words)
    })

# Exportação dos Dados
df_top_termos = pd.DataFrame(dados_tabela)
df_top_termos.to_csv("outputs/tabela_top_termos_mensais.csv", index=False, encoding='utf-8')
print("Tabela gerada com sucesso: 'outputs/tabela_top_termos_mensais.csv'")

df_monthly.to_parquet("outputs/tabnews_monthly_cleaned.parquet")
print("Base de textos processada exportada: 'outputs/tabnews_monthly_cleaned.parquet'")