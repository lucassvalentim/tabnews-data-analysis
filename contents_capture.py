import pandas as pd
import time
import requests

BASE_URL = "https://www.tabnews.com.br/api/v1"

df_posts = pd.read_csv('csv/posts_file.csv')

columns_posts = [
    "id", # id do post
    "body"
]

all_contents = []

headers = {
    "User-Agent": "Mozilla/5.0"
}

for row in df_posts.itertuples(index=True):     
    url = f"{BASE_URL}/contents/{row.owner_username}/{row.slug}"

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10, headers=headers)
            
            if response.status_code == 200:
                all_contents.append(response.json())
                print(f"Conteudo do usuario {row.owner_username} capturado com sucesso")
                break
            
            elif response.status_code == 429:
                print("Rate limit... esperando")
                time.sleep(5)
            
            else:
                print(f"Erro {response.status_code} do conteudo o usuario {row.owner_username}")
                time.sleep(5)
        
        except requests.exceptions.ConnectionError:
            print(f"Conexão caiu (tentativa {attempt+1})")
            time.sleep(2 ** attempt)

df_contents = pd.DataFrame(all_contents, columns=columns_posts)
df_contents.to_csv('contents.csv', index=False)