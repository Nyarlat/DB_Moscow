from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast
import torch


MODEL_SPELL = 'UrukHan/t5-russian-spell'
MAX_INPUT = 512

# Загрузка модели и токенизатора
spell_tokenizer = T5TokenizerFast.from_pretrained(MODEL_SPELL)
spell_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_SPELL)

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
spell_model.to(device)


def spell_text(input_sequences):
    task_prefix = "Spell correct: "
    if type(input_sequences) != list: input_sequences = [input_sequences]
    encoded = spell_tokenizer(
        [task_prefix + sequence for sequence in input_sequences],
        padding="longest",
        max_length=MAX_INPUT,
        truncation=True,
        return_tensors="pt",
    )

    encoded.to(device)
    predicts = spell_model.generate(**encoded)
    new_text = spell_tokenizer.batch_decode(predicts, skip_special_tokens=True)
    return " ".join(new_text)
