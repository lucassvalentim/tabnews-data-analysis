import pandas as pd
import time
import requests
import csv

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
    "children_deep_count"
]

def flatten_comments(comments):
    flatten_list = []
    for comment in comments:
        comment_data = {k: v for k, v in comment.items() if k != 'children'}

        flatten_list.append(comment_data)

        if comment.get('children'):
            flatten_list.extend(flatten_comments(comment['children']))

    return flatten_list

all_comments = []

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Accept": "application/json"
}

for row in df_posts.itertuples(index=True):     

    if row.Index >= 100:
        break

    url = f"{BASE_URL}/contents/{row.owner_username}/{row.slug}/children"
    
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10, headers=headers)
            
            if response.status_code == 200:
                print("=============")
                print(f"Comentario do usuario {row.owner_username} capturado com sucesso")
                print(f"Usuario da linha {row.Index}")
                print("=============")

                data_response = response.json()
                
                flattened = flatten_comments(data_response)
                all_comments.extend(flattened)

                time.sleep(1)
                break
            
            elif response.status_code == 429:
                print("429 Rate limit... esperando")
                time.sleep(5)
            
            elif response.status_code == 403:
                print("403 Rate limit... esperando")
                time.sleep(30)
            
            else:
                print(f"Erro {response.status_code} do comentario o usuario {row.owner_username}")
                time.sleep(5)
        
        except requests.exceptions.ConnectionError:
            print(f"Conexão caiu (tentativa {attempt+1})")
            time.sleep(2 ** attempt)

total_coments = 0
for comment in all_comments:
    total_coments += int(comment["children_deep_count"])

print(f"Total comment: {total_coments}")

df_comments = pd.DataFrame(all_comments, columns=columns_coments)
df_comments.to_csv(
    "comments.csv",
    index=False,
    encoding="utf-8",
    quoting=csv.QUOTE_ALL,      # coloca aspas em tudo
    escapechar="\\",            # escapa caracteres especiais
)