import re
import pymorphy2
from nltk.corpus import stopwords
from nltk import word_tokenize, download

#стоп-слова
download('stopwords')


class TextPreprocessor:
    """
    Класс для предобработки текста. Предоставляет возможность удаления стоп-слов и лемматизации текста.

    :param remove_stopwords: Флаг для удаления стоп-слов (по умолчанию True)
    :param lemmatization: Флаг для лемматизации слов (по умолчанию False)
    """
    def __init__(self, remove_stopwords: bool = True,
                 lemmatization: bool = False):
        self.lemmatization = lemmatization
        self.remove_stopwords = remove_stopwords
        self.morph = pymorphy2.MorphAnalyzer()
        self.stopwords = stopwords.words("russian")

    def _remove_stopwords(self, tokens: list[str]):
        """
        Удаляет стоп-слова из списка токенов.

        :param tokens: Список токенов (слов)
        :return: Список токенов без стоп-слов
        """
        return [token for token in tokens if token not in self.stopwords]

    def _lemmatize_text(self, tokens: list[str]):
        """
        Лемматизирует список токенов, приводя слова к их нормальной форме.

        :param tokens: Список токенов (слов)
        :return: Лемматизированный список токенов
        """
        return [self.morph.parse(token)[0].normal_form for token in tokens if re.match(r'\w+', token)]

    def preprocess(self, text: str) -> str:
        """
        Выполняет полную предобработку текста: приведение к нижнему регистру, удаление ссылок,
        хештегов, эмодзи, лишних пробелов, а также удаление стоп-слов и лемматизация.

        :param text: Входной текст для предобработки
        :return: Предобработанный текст
        """
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


