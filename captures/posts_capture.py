import requests
import pandas as pd
import time

BASE_URL = "https://www.tabnews.com.br/api/v1"

columns_posts = [
    "id",
    "owner_id",
    "parent_id",
    "slug",
    "title",
    "status",
    "source_url",
    "created_at",
    "updated_at",
    "published_at",
    "deleted_at",
    "tabcoins",
    "tabcoins_credit",
    "tabcoins_debit",
    "owner_username",
    "children_deep_count",
    "type"
]

def pages_capture(page):
    print("============================ INICIANDO A CAPTURA DOS DADOS ============================")
    
    all_pages = []
    
    for i in range(1, page + 1):
        url = f"{BASE_URL}/contents?page={i}&strategy=new"
        
        retries = 3
        
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    all_pages.append(response.json())
                    print(f"Página {i} capturada com sucesso")
                    break
                
                elif response.status_code == 429:
                    print("Rate limit atingido. Aguardando...")
                    time.sleep(5)
                
                else:
                    print(f"Erro {response.status_code} na página {i}")
                    time.sleep(2)
            
            except requests.exceptions.RequestException as e:
                print(f"Erro de conexão na página {i}: {e}")
                time.sleep(2)
        
        #delay entre requisições
        time.sleep(0.5)
    
    print("============================ FIM DA CAPTURA DOS DADOS ==================================")
    
    return all_pages


all_pages = pages_capture(975)
posts = []
total_coments = 0
for page in all_pages:
    for post in page:
        posts.append(post)
        
        total_coments += post["children_deep_count"]

df = pd.DataFrame(posts, columns= columns_posts)
df.to_parquet('../data/tabnews_data.parquet', index=False)

print(f"Total de comentarios: {total_coments}")
