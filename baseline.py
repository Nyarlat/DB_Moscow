import pandas as pd
from sentence_transformers import SentenceTransformer
import json
from tqdm.autonotebook import tqdm
import numpy as np
import faiss


data = pd.read_csv("train_data_categories.csv")[['video_id', 'title', 'description']]
taxonomy = pd.read_csv("IAB_tags.csv")

print(data.columns)
print(data.head(5))

print(taxonomy.head(5))
print(taxonomy.columns)

model = SentenceTransformer('DeepPavlov/rubert-base-cased-sentence', )
dim = 768 # размер вектора эмбеддинга


# СЮДА ДОБАВЛЯТЬ СТОЛБЦЫ
data['title_vector'] = data.apply(lambda row: model.encode(f"{row['title']} {row['description']}", convert_to_tensor=True).cpu().numpy(),axis=1)


def get_tags():
    tags = {}
    for i, row in tqdm(taxonomy.iterrows()):
        if isinstance(row['Уровень 1 (iab)'], str):
            tags[row['Уровень 1 (iab)']] = model.encode(row['Уровень 1 (iab)'], convert_to_tensor=True).cpu().numpy()#.tolist()
        if isinstance(row['Уровень 2 (iab)'], str):
            tags[row['Уровень 1 (iab)']+ ": "+row['Уровень 2 (iab)']] = model.encode(row['Уровень 1 (iab)']+ ": "+row['Уровень 2 (iab)'], convert_to_tensor=True).cpu().numpy()#.tolist()
        if isinstance(row['Уровень 3 (iab)'], str):
            tags[row['Уровень 1 (iab)'] + ": "+row['Уровень 2 (iab)']+": "+row['Уровень 3 (iab)']] = model.encode(row['Уровень 1 (iab)']+ ": "+row['Уровень 2 (iab)']+": "+row['Уровень 3 (iab)'], convert_to_tensor=True).cpu().numpy()#.tolist()
    return tags


tags = get_tags()
tags_list = list(tags.keys())
vectors = np.array(list(tags.values()))

index = faiss.index_factory(dim, "Flat", faiss.METRIC_INNER_PRODUCT)
print(index.ntotal)
index.add(vectors)
print(index.ntotal)

normalized_scores = []
filtered_scores = []


topn = 10
sample_submission = pd.DataFrame(data=data['video_id'].to_list(), columns=['video_id'])
sample_submission['predicted_tags']=np.nan
sample_submission['predicted_tags'] = sample_submission['predicted_tags'].astype('object')


threshold = 0.1

for i, row in data.iterrows():
    scores, predictions = index.search(np.array([row['title_vector']]), topn)

    normalized_scores = scores[0] / max(scores[0]) if max(scores[0]) > 0 else scores[0]

    filtered_tags = [tags_list[predictions[0][j]] for j in range(len(normalized_scores)) if
                     normalized_scores[j] <= threshold]

    index_i = sample_submission[sample_submission.video_id == row.video_id].index
    sample_submission.at[index_i[0], 'predicted_tags'] = filtered_tags if filtered_tags else [None]

sample_submission.to_csv("sample_submission.csv", index_label=0)
