import pandas as pd
import time
import requests

BASE_URL = "https://www.tabnews.com.br/api/v1"

df_posts = pd.read_parquet('data/tabnews_data.parquet')

columns_posts = ["id", "body"]

all_contents = []
failed_posts = []

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Accept": "application/json"
}

for row in df_posts.itertuples(index=True):
    url = f"{BASE_URL}/contents/{row.owner_username}/{row.slug}"
    
    success = False        
    last_reason = "Desconhecido"
    
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=15, headers=headers)
            
            if response.status_code == 200:
                all_contents.append(response.json())
                print("=============")
                print(f"Conteúdo do usuário {row.owner_username} capturado com sucesso")
                print(f"Usuário da linha {row.Index}")
                print("=============")
                time.sleep(1)
                success = True 
                break           # Sai do loop de tentativas (retries)
            
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

if all_contents:
    df_contents = pd.DataFrame(all_contents, columns=columns_posts)
    df_contents.to_parquet("data/tabnews_contents.parquet", index=False)
    print(f"\n{len(all_contents)} posts salvos em 'data/tabnews_contents.parquet'.")
else:
    print("\nNenhum post foi capturado com sucesso.")

# Salvamento de erros
if failed_posts:
    df_errors = pd.DataFrame(failed_posts)
    df_errors.to_parquet("../data/erros_contents.parquet", index=False)
    print(f"ALERTA: {len(failed_posts)} posts falharam e foram registrados em 'data/erros_contents.parquet'.")
else:
    print("Sucesso total! Nenhum post falhou.")

print("Processo finalizado!")