from joblib import dump, load
from typing import Optional, Union
import pandas as pd
import numpy as np
from text_preprocessing import TextPreprocessor
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split


class LogRegPipeline:
    def __init__(self, filename: str = None):
        if filename:
            print("Load from file...")
            self.pipeline = load(filename)
        else:
            print("Model not found. Start training on dataset")
            self.pipeline = self._train()
            print("Model has been trained. Saving ...")
            self.save("../models/tf_idf_knn.joblib")

    def _train(self) -> Pipeline:
        # ('clf', LogisticRegression(n_jobs=1, C=1e5, max_iter=1000))
        pipeline = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', KNeighborsClassifier())])

        df = pd.read_csv("../test_data/train_data.csv")
        df.dropna(inplace=True)
        df.drop(columns=["video_id"], inplace=True)

        df["tags"] = df["tags"].str.replace('%', ':', regex=False).str.replace('\t', ':', regex=False)
        df["tags"] = df["tags"].apply(lambda l: l.split(', '))
        df["tags"] = df["tags"].apply(lambda x: x[0])

        df["c1"] = df["tags"].apply(lambda x: self._get_main_category(x))
        df = df.replace("", np.nan).dropna(subset=["c1"])
        df_filtered = df.groupby('c1').filter(lambda g: len(g) > 1)

        new_df = df_filtered.copy()
        preprocessor = TextPreprocessor(lemmatization=True)
        new_df["description"] = (new_df["description"] + new_df["video2text"].astype(str)).apply(lambda x: preprocessor.preprocess(x))

        pipeline.fit(new_df["description"], new_df["c1"])
        return pipeline

    def save(self, filename: str):
        print("Save to file")
        dump(self.pipeline, filename)

    def predict(self, text: Union[str, list[str]]) -> list[str]:
        if isinstance(text, str):
            text = [text]
        return self.pipeline.predict(text)

    @staticmethod
    def _get_main_category(tags):
        main_categories = []
        if isinstance(tags, str):
            tags = [tags]
        for tag in tags:
            tag = tag.split(":")[0].replace('\n', '').strip()
            if tag not in main_categories:
                main_categories.append(tag)
        return main_categories[0]


