import os
import pandas as pd
from ml.speech2text import speech_recognition
from ml.video2text import get_text_from_video


def create_train_data(df_path, video_folder):
    # Загрузка данных из CSV файла
    df = pd.read_csv(df_path)

    # Функция для проверки существования файла и получения текста
    def process_video(video_name):
        video_path = f"{video_folder}/{video_name}.mp4"
        if os.path.exists(video_path):
            speech_text = speech_recognition(video_path)
            video_text = get_text_from_video(video_path)
            return speech_text, video_text
        else:
            print(f"Файл {video_path} не найден. Пропускаем.")
            return "", ""

    # Применение функции к каждому видео и создание новых столбцов
    df['speech2text'], df['video2text'] = zip(*df['video_id'].apply(process_video))

    # Сохранение обновленного DataFrame в новый CSV файл
    df.to_csv('train_data.csv', index=False)


if __name__ == "__main__":
    create_train_data(df_path="D:/train_data_categories.csv",
                      video_folder="D:/videos")
