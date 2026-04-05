import pandas as pd
import time
import requests

BASE_URL = "https://www.tabnews.com.br/api/v1"

df_posts = pd.read_csv('csv/posts_file.csv')

# def contents_capture(page):
columns_coments = [
    "id",
    "parent_id",
    "owner_id",
    "slug",
    "title",
    "body",
    "status",
    "source_url",
    "published_at",
    "created_at",
    "updated_at",
    "deleted_at",
    "type",
    "owner_username",
    "tabcoins",
    "tabcoins_credit",
    "tabcoins_debit",
    "children",
    "children_deep_count"
]

all_coments = []

session = requests.Session()

for row in df_posts.itertuples(index=True):     
    if row.Index == 3:
        break

    url = f"{BASE_URL}/contents/{row.owner_username}/{row.slug}/children"

    retries = 3
    for attempt in range(retries):
        try:
            response = session.get(url, timeout=10)
            
            if response.status_code == 200:
                all_coments.append(response.json())
                print(f"Comentario do usuario {row.owner_username} capturado com sucesso")
                break
            
            elif response.status_code == 429:
                print("Rate limit... esperando")
                time.sleep(5)
            
            else:
                print(f"Erro {response.status_code} do comentario do usuario {row.owner_username}")
                time.sleep(2)
        
        except requests.exceptions.ConnectionError:
            print(f"Conexão caiu (tentativa {attempt+1})")
            time.sleep(2 ** attempt)

print(all_coments)
# df_contents = pd.DataFrame(all_contents, columns=columns_posts)
# df_contents.to_csv('contents.csv', index=False)