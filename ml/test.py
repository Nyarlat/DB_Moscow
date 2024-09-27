import time
from speech2text import speech_recognition
from spellcast import spell_text

if __name__ == '__main__':
    models = {1: "tiny", 2: "small", 3: "base", 4: "medium", 5: 'large'}

    # Менять цифру для замены модели
    model = 3

    start_time = time.time()
    speech_text = speech_recognition(video_path="video.mp4", model=models[model])
    elapsed_recognition_time = time.time() - start_time
    print(f"Время выполнения распознавания речи : {elapsed_recognition_time:.2f} секунд")

    with open(f"speech_text_{models[model]}.txt", 'w') as file:
        file.write(speech_text)

    start_time = time.time()

    # Делим текст на предложения, чтобы spellcast смог обработать
    # Иначе он упрется в потолок токенов
    # Наверно лучше не юзать spellcast
    spelled_text = ""

    for seq in speech_text.split(". "):
        spelled_text += spell_text(seq) + " "
    elapsed_spell_time = time.time() - start_time

    with open(f"spelled_text_{models[model]}.txt", 'w') as file:
        file.write(spelled_text)

    print(f"Время выполнения spellcast: {elapsed_spell_time:.2f} секунд")
    print(f"Общее время выполнения: {elapsed_recognition_time+elapsed_spell_time:.2f} секунд")
