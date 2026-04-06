import pandas as pd;

df = pd.read_csv('comments.csv')
print(len(df))

# inputs = [{'id': '14cd6d95-ff01-4104-92af-5f57cce604fc', 
#           'owner_id': 'c9d0007f-4fcf-44cd-826e-16a7eb0ea174', 
#           'parent_id': None, 
#           'slug': 'deep-links-em-flutter-sem-pacotes-do-zero-ate-producao-parte-1', 
#           'title': 'Deep Links em Flutter sem pacotes: do zero até produção (Parte 1)', 
#           'status': 'published', 
#           'source_url': 'https://medium.com/p/d56ea3619192?postPublishedType=initial', 
#           'created_at': '2026-04-04T19:04:29.449Z', 
#           'updated_at': '2026-04-04T19:04:29.449Z', 
#           'published_at': '2026-04-04T19:04:29.454Z', 
#           'deleted_at': None, 
#           'tabcoins': 6, 
#           'tabcoins_credit': 5,
#           'tabcoins_debit': 0,
#           'owner_username': 'crdornelles',
#           'children_deep_count': 0, 
#           'type': 'content'
#           },
#           {
#               'id': '190cf3af-db38-4f5b-b56a-835176353a64', 
#               'owner_id': 'f8b096bb-e90f-43ba-ac8b-25cf0748cb0c', 
#               'parent_id': None, 
#               'slug': 'criou-varios-agentes-de-ia-e-agora-ta-perdido-nomes-comandos-quando-usar-cada-um-tenho-a-solucao', 
#               'title': 'Criou vários agentes de IA e agora tá perdido? Nomes, comandos, quando usar cada um... Tenho a solução.', 
#               'status': 'published', 
#               'source_url': None, 
#               'created_at': '2026-04-04T15:10:53.724Z', 
#               'updated_at': '2026-04-04T15:10:53.724Z', 
#               'published_at': '2026-04-04T15:10:53.738Z', 
#               'deleted_at': None, 
#               'tabcoins': 4, 
#               'tabcoins_credit': 3, 
#               'tabcoins_debit': 0, 
#               'owner_username': 'LucasMattos', 
#               'children_deep_count': 0, 
#               'type': 'content'
#               }]


# columns = [
#     "id",
#     "owner_id",
#     "parent_id",
#     "slug",
#     "title",
#     "status",
#     "source_url",
#     "created_at",
#     "updated_at",
#     "published_at",
#     "deleted_at",
#     "tabcoins",
#     "tabcoins_credit",
#     "tabcoins_debit",
#     "owner_username",
#     "children_deep_count",
#     "type"
# ]

# df = pd.DataFrame(inputs, columns= columns)
# df.to_csv('my_file.csv', index=False)
# print(df)
# data = []
# d = {}
# for colum in columns:
#     d[columns] = inputs[colum] 

# df_interactions = pd.read_csv('interactions.csv')
# df_posts = pd.read_csv('posts.csv')
# print(df_posts["author"].value_counts())
# print(df_interactions.groupby(["from_user", "to_user"]).size())