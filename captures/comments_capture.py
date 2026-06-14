import pandas as pd
import time
import requests
import csv

BASE_URL = "https://www.tabnews.com.br/api/v1"

df_posts = pd.read_parquet('data/tabnews_data.parquet')

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
failed_posts = []

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Accept": "application/json"
}

for row in df_posts.itertuples(index=True):     
    url = f"{BASE_URL}/contents/{row.owner_username}/{row.slug}/children"
    
    success = False        
    last_reason = "Desconhecido"

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=15, headers=headers)
            
            if response.status_code == 200:
                print("=============")
                print(f"Comentario do usuario {row.owner_username} capturado com sucesso")
                print(f"Usuario da linha {row.Index}")
                print("=============")

                data_response = response.json()
                
                flattened = flatten_comments(data_response)
                all_comments.extend(flattened)

                time.sleep(1)
                sucess = True
                break
            
            elif response.status_code == 429:
                last_reason = "Erro 429 (Rate limit)"
                print("Rate limit atingido... esperando 5 segundos")
                time.sleep(5)
            
            elif response.status_code == 403:
                last_reason = "Erro 403 (Forbidden/Cloudflare)"
                print("Acesso proibido... esperando 30 segundos")
                time.sleep(30)
            
            else:
                last_reason = f"Erro HTTP {response.status_code}"
                print(f"{last_reason} no conteúdo do usuário {row.owner_username}")
                time.sleep(5)
        
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            last_reason = "Erro de Conexão ou Timeout"
            print(f"O servidor demorou para responder ou a conexão caiu (tentativa {attempt+1}/{retries})")
            time.sleep(2 ** attempt)
    
    # Caso o posto não foi capturado com sucesso:
    if not success:
        failed_posts.append({
            "id": getattr(row, 'id', None),
            "owner_username": row.owner_username,
            "slug": row.slug,
            "motivo_erro": last_reason
        })

if all_comments:
    df_comments = pd.DataFrame(all_comments, columns=columns_coments)
    df_comments.to_parquet("data/tabnews_comments.parquet", index=False)
    print(f"\n{len(all_comments)} posts salvos em 'data/tabnews_comments.parquet'.")
    
    total_comments, _ = df_comments.shape
    print(f"Total de comentarios: {total_comments}")
else:
    print("\nNenhum post foi capturado com sucesso.")

# Salvamento de erros
if failed_posts:
    df_errors = pd.DataFrame(failed_posts)
    df_errors.to_parquet("../data/erros_comments.parquet", index=False)
    print(f"ALERTA: {len(failed_posts)} posts falharam e foram registrados em 'data/erros_comments.parquet'.")
else:
    print("Sucesso total! Nenhum post falhou.")

print("Processo finalizado!")