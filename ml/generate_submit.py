from utils import flatten_hierarchy
from const import MODEL_ZERO, HIERARCHY
from zero_shooter import ZeroShooter
from classification_models import LogRegPipeline
import torch
import pandas as pd
import time
from text_preprocessing import TextPreprocessor

logreg = LogRegPipeline()
zero_shooter = ZeroShooter(model_name=MODEL_ZERO, device=torch.device("cuda"), logreg=logreg)
preprocessor = TextPreprocessor(lemmatization=True)

df = pd.read_csv("../data/test_data.csv")
data = df.copy()
data["description"] = data["description"] + data["video2text"].astype(str)
data["description"] = data["description"] + data["speech2text"]
data["description"] = data["description"].apply(lambda x: preprocessor.preprocess(x))

start = time.time()
data["predicted_tags"] = data["description"].apply(
    lambda x: flatten_hierarchy(zero_shooter.recursive_classify_logreg(text=x,
                                                                hierarchy=HIERARCHY,
                                                                threshold=None)))

data = data[["video_id", "predicted_tags"]]
data.to_csv("../data/test_sub_ps_knn_zero_video.csv", sep=",", index=False)

print(time.time() - start)
