import re
import pymorphy2
from nltk.corpus import stopwords
from nltk import word_tokenize, download

download('stopwords')


class TextPreprocessor:
    def __init__(self, remove_stopwords: bool = True,
                 lemmatization: bool = False):
        self.lemmatization = lemmatization
        self.remove_stopwords = remove_stopwords
        self.morph = pymorphy2.MorphAnalyzer()
        self.stopwords = stopwords.words("russian")

    def _remove_stopwords(self, tokens: list[str]):
        return [token for token in tokens if token not in self.stopwords]

    def _lemmatize_text(self, tokens: list[str]):
        return [self.morph.parse(token)[0].normal_form for token in tokens if re.match(r'\w+', token)]

    def preprocess(self, text: str) -> str:
        text = text.lower()

        text = re.sub(r'http[s]?://\S+|www\.\S+', '', text)  # Удаление ссылок (URL)
        text = re.sub(r'#\w+', '', text)  # Удаление хештегов
        text = re.sub(r'[^\w\s]', '', text)  # Удаление эмодзи
        text = re.sub(r'\s+', ' ', text).strip()  # Удаление лишних пробелов

        tokens = word_tokenize(text, language="russian")

        if self.remove_stopwords:
            tokens = self._remove_stopwords(tokens)

        if self.lemmatization:
            tokens = self._lemmatize_text(tokens)

        return " ".join(tokens)


