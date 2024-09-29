import os
import time
import pandas as pd
from ml.speech2text import speech_recognition
from ml.video2text import get_text_from_video


def create_train_data(df_path, video_folder):
    # Создаем файл для хранения результатов
    output_file = 'train_data.csv'

    # Удаляем файл, если он уже существует, чтобы избежать дублирования
    if os.path.exists(output_file):
        os.remove(output_file)

    total = len(os.listdir(video_folder))
    processed_count = 0

    # Чтение CSV файла по частям
    for chunk in pd.read_csv(df_path, chunksize=100):
        # Функция для обработки видео
        def process_video(video_name):
            nonlocal processed_count

            video_path = f"{video_folder}/{video_name}.mp4"
            if os.path.exists(video_path):
                speech_text = ""
                video_text = ""
                try:
                    speech_text = speech_recognition(video_path)
                except Exception as e:
                    print(f"Ошибка при обработке речи в {video_path}: {e}")

                try:
                    video_text = get_text_from_video(video_path)
                except Exception as e:
                    print(f"Ошибка при обработке кадров в {video_path}: {e}")

                processed_count += 1
                print(f"Обработано файлов: {processed_count} из {total}")

                return speech_text, video_text

            else:
                print(f"Файл {video_path} не найден. Пропускаем.")
                return "", ""

        # Применение функции к каждому видео и создание новых столбцов
        chunk['speech2text'], chunk['video2text'] = zip(*chunk['video_id'].apply(process_video))

        # Сохранение обновленного чанка в CSV файл
        chunk.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)


def get_tags(video_path, video_name, video_desc):
    start_time = time.time()
    speech_text = ""
    video_text = ""

    if os.path.exists(video_path):
        try:
            speech_text = speech_recognition(video_path)
        except Exception as e:
            print(f"Ошибка при обработке речи в {video_path}: {e}")
        try:
            video_text = get_text_from_video(video_path)
        except Exception as e:
            print(f"Ошибка при обработке кадров в {video_path}: {e}")
    else:
        print(f"Файл {video_path} не найден. Пропускаем.")

    tags = ['Машиностроение', 'Государственные закупки', 'Информационно-развлекательные технологии']  # mock
    elapsed_time = time.time() - start_time
    print(f"Время выполнения обработки видео {video_path}: {elapsed_time:.2f} секунд")
    return tags, speech_text, video_text


if __name__ == "__main__":
    create_train_data(df_path="D:/test_tag_video/sample_submission.csv",
                      video_folder="D:/test_tag_video/videos")
