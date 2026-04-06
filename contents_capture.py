import pandas as pd
import time
import requests
import csv

BASE_URL = "https://www.tabnews.com.br/api/v1"

df_posts = pd.read_csv('csv/posts_file.csv')

columns_posts = [
    "id", # id do post
    "body"
]

all_contents = []

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Accept": "application/json"
}

content_lengh = 50
for row in df_posts.itertuples(index=True):

    if row.Index >= content_lengh:
        break


    url = f"{BASE_URL}/contents/{row.owner_username}/{row.slug}"

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10, headers=headers)
            
            if response.status_code == 200:
                all_contents.append(response.json())
                print("=============")
                print(f"Conteudo do usuario {row.owner_username} capturado com sucesso")
                print(f"Usuario da linha {row.Index}")
                print("=============")
                time.sleep(1)
                break
            
            elif response.status_code == 429:
                print("Rate limit... esperando")
                time.sleep(5)
            
            elif response.status_code == 403:
                print("Rate limit... esperando")
                time.sleep(30)
            
            else:
                print(f"Erro {response.status_code} do conteudo o usuario {row.owner_username}")
                time.sleep(5)
        
        except requests.exceptions.ConnectionError:
            print(f"Conexão caiu (tentativa {attempt+1})")
            time.sleep(2 ** attempt)

df_contents = pd.DataFrame(all_contents, columns=columns_posts)
df_contents.to_csv(
    "dados.csv",
    index=False,
    encoding="utf-8",
    quoting=csv.QUOTE_ALL,      # coloca aspas em tudo
    escapechar="\\",            # escapa caracteres especiais
)