import pandas as pd

df_content = pd.read_parquet('data/tabnews_contents.parquet')
df_posts = pd.read_parquet('data/tabnews_data.parquet')
df_erros = pd.read_parquet("data/erros.parquet")

print(df_posts)
# IDs dos posts que não foram possíveis capturar o conteúdo
ids_com_erros = df_erros['id']

# IDs dos posts da NewsletterOficial
id_posts_delete = df_posts.loc[
    df_posts['owner_username'] == 'NewsletterOficial',
    'id'
]

# atualiza o df_posts sem os que nao foram possíveis capturar
df_posts = df_posts[
    ~df_posts["id"].isin(ids_com_erros)
].copy()

print(df_posts)
# Remove do df_posts
df_filtered_p = df_posts[
    df_posts['owner_username'] != 'NewsletterOficial'
].copy()

# Remove do df_content os conteúdos desses posts
df_filtered_c = df_content[
    ~df_content['id'].isin(id_posts_delete)
].copy()


print(df_filtered_c)

df_filtered_p = df_filtered_p.merge(
    df_filtered_c[['id', 'body']],
    on='id',
    how='left'
)
print(f"Tamanho do df_posts original: {df_posts.shape}")
print(f"Tamanho do df_posts filtrado: {df_filtered_p.shape}")

print(f"Tamanho do df_content original: {df_content.shape}")
print(f"Tamanho do df_content filtrado: {df_filtered_c.shape}")

print(df_filtered_p)