import whisper
import os
import ffmpeg


def extract_audio_from_video(video_path, audio_path):
    """
    Извлекает аудио из видеофайла
    :param video_path: Путь к видеофайлу
    :param audio_path: Путь, куда будет сохранен аудиофайл
    """
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, format='wav', ac=1, ar='16000')
            .run(overwrite_output=True)
        )
    except Exception as e:
        print(f"Error extracting audio: {e}")


def trim_audio(audio_path, max_duration=600):
    """
    Обрезает аудиофайл до максимальной продолжительности.
    :param audio_path: Путь к аудиофайлу, который нужно обрезать
    """
    try:
        trimmed_audio_path = "trimmed_" + audio_path  # Create a new file for trimmed audio
        (
            ffmpeg
            .input(audio_path, ss=0, t=max_duration)
            .output(trimmed_audio_path)
            .run(overwrite_output=True)
        )
        os.replace(trimmed_audio_path, audio_path)  # Replace original with trimmed audio
    except Exception as e:
        print(f"Error trimming audio: {e}")


def speech_recognition(video_path, model='base'):
    """
     Распознавание речи из аудио, извлеченного из видеофайла.
    :param video_path: Путь к видеофайлу
    :param model: Whisper для распознавания речи
    """
    audio_path = "audio.wav"

    # Загрузка модели Whisper для распознавания речи
    speech_model = whisper.load_model(model, device="cuda")

    # Извлекаем и обрезаем аудио
    extract_audio_from_video(video_path, audio_path)
    trim_audio(audio_path)

    # Выполняем транскрипцию обрезанного аудио
    try:
        result = speech_model.transcribe(audio_path, language='ru')
        return result['text']
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
    finally:
        # Удаляем временный аудиофайл
        if os.path.exists(audio_path):
            os.remove(audio_path)


if __name__ == "__main__":
    print(speech_recognition('663ac16d23ef52bd261af0a41e6d8f6b.mp4'))
