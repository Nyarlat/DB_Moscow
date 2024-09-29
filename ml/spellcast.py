from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast
import torch

MODEL_SPELL = 'UrukHan/t5-russian-spell'
MAX_INPUT = 512

# Загрузка токенизатора и модели для выполнения задачи коррекции орфографии
spell_tokenizer = T5TokenizerFast.from_pretrained(MODEL_SPELL)
spell_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_SPELL)

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
spell_model.to(device)  # Переносим модель на выбранное устройство


def spell_text(input_sequences):
    """
    Корректирует орфографические ошибки в переданном тексте с использованием предобученной модели.
    :param input_sequences: Входная строка или список строк с текстом для коррекции
    :return: Исправленный текст
    """
    if not isinstance(input_sequences, str):
        return ""  # Если входные данные не строка, возвращаем пустую строку

    # Префикс задачи, который нужен для корректного использования модели T5
    task_prefix = "Spell correct: "

    # Если input_sequences — не список, преобразуем его в список
    if type(input_sequences) != list:
        input_sequences = [input_sequences]

    # Токенизируем входные данные с добавлением префикса задачи
    encoded = spell_tokenizer(
        [task_prefix + sequence for sequence in input_sequences],  # Добавляем префикс задачи к каждому предложению
        padding="longest",  # Добавляем паддинг к самому длинному предложению для выравнивания длины входных данных
        max_length=MAX_INPUT,  # Ограничиваем максимальную длину входных данных
        truncation=True,  # Обрезаем предложения, превышающие max_length
        return_tensors="pt",  # Возвращаем данные в формате тензоров PyTorch
    )

    encoded.to(device)

    # Генерируем исправленный текст с использованием модели
    predicts = spell_model.generate(**encoded)

    # Декодируем результат из тензоров обратно в текст
    new_text = spell_tokenizer.batch_decode(predicts, skip_special_tokens=True)

    # Объединяем список предложений в одну строку и возвращаем результат
    return " ".join(new_text)