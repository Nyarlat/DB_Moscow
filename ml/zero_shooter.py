import torch
import numpy as np
from itertools import product
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


class ZeroShooter:
    def __init__(self,  model_name: str, device: torch.device = None, logreg=None):
        if not device:
            device = torch.device("cpu")

        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.device = device
        self.classifier = pipeline(task="zero-shot-classification",
                                   model=self.model,
                                   tokenizer=self.tokenizer,
                                   device=self.device)
        self.logreg = logreg

    def classify(self, texts, labels: list[str], only_predicted_label: bool = False):
        predicts = self.classifier(texts, labels, multi_label=True, batch_size=16)
        if only_predicted_label:
            # return [pred["labels"][0] for pred in predicts]
            return predicts["labels"][0]
        return predicts


    def recursive_classify(self, text, hierarchy, threshold: float = None):
        if not hierarchy:
            return {}

        current_level = list(hierarchy.keys())

        predict = self.classifier(text, current_level, multi_label=True, batch_size=64)
        proba = predict["scores"]

        if threshold:
            selected_cats = [a for a, b in zip(predict["labels"], proba) if b > threshold]
            if len(selected_cats) == 0:
                selected_cats = [predict["labels"][proba.index(max(proba))]]
        else:
            selected_cats = [predict["labels"][proba.index(max(proba))]]
        result = {}

        for label in selected_cats:
            next_level = hierarchy.get(label, {})

            if isinstance(next_level, list):

                if next_level:
                    predict_next = self.classifier(text, next_level, multi_label=True, batch_size=64)
                    proba_next = predict_next["scores"]

                    if threshold:
                        next_level_cats = [a for a, b in zip(predict_next["labels"], proba_next) if b > threshold]
                        if len(next_level_cats) == 0:
                            next_level_cats = [predict_next["labels"][proba_next.index(max(proba_next))]]
                    else:
                        next_level_cats = [predict_next["labels"][proba_next.index(max(proba_next))]]

                    result[label] = {cat: {} for cat in next_level_cats}
                else:
                    result[label] = {}
            else:
                result[label] = self.recursive_classify(text, next_level, threshold)

        return result


    def recursive_classify_logreg(self, text, hierarchy, threshold: float = None, first_level=True):
        if not hierarchy:
            return {}

        current_level = list(hierarchy.keys())

        if first_level:
            selected_cats = self.logreg.predict(text)
            first_level = False
        else:
            predict = self.classifier(text, current_level, multi_label=True, batch_size=64)
            proba = predict["scores"]

            if threshold:
                selected_cats = [a for a, b in zip(predict["labels"], proba) if b > threshold]
                if len(selected_cats) == 0:
                    selected_cats = [predict["labels"][proba.index(max(proba))]]
            else:
                selected_cats = [predict["labels"][proba.index(max(proba))]]

        result = {}

        for label in selected_cats:
            next_level = hierarchy.get(label, {})

            if isinstance(next_level, list):

                if next_level:
                    predict_next = self.classifier(text, next_level, multi_label=True, batch_size=64)
                    proba_next = predict_next["scores"]

                    if threshold:
                        next_level_cats = [a for a, b in zip(predict_next["labels"], proba_next) if b > threshold]
                        if len(next_level_cats) == 0:
                            next_level_cats = [predict_next["labels"][proba_next.index(max(proba_next))]]
                    else:
                        next_level_cats = [predict_next["labels"][proba_next.index(max(proba_next))]]

                    result[label] = {cat: {} for cat in next_level_cats}
                else:
                    result[label] = {}
            else:
                result[label] = self.recursive_classify_logreg(text, next_level, threshold, first_level=first_level)

        return result





