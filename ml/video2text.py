import cv2
import os
from PIL import Image
from googletrans import Translator
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to("cuda")

traslator = Translator()


def extract_frames(video_path, frames_to_extract=10):
    # Открываем видео файл
    cap = cv2.VideoCapture(video_path)

    # Получаем общее количество кадров и частоту кадров
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Вычисляем длительность видео в секундах
    video_duration = total_frames / fps

    # Вычисляем количество кадров для извлечения
    interval = video_duration / frames_to_extract

    extracted_frames = []

    for i in range(frames_to_extract):
        # Вычисляем время для текущего кадра
        current_time = i * interval

        # Перемещаемся к нужному кадру
        cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)

        # Читаем кадр
        ret, frame = cap.read()

        if ret:
            extracted_frames.append(frame)
        else:
            continue

    cap.release()

    return extracted_frames


def get_text_from_frame(frame_path, cond_text="a frame of"):
    raw_image = Image.open(frame_path).convert('RGB')

    inputs = processor(raw_image, cond_text, return_tensors="pt").to("cuda")

    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True).capitalize()


def get_text_from_video(video_path):
    text = ""
    frames = extract_frames(video_path)

    # Сохранение извлеченных кадров (опционально)
    for idx, frame in enumerate(frames):
        frame_path = f'frame_{idx + 1}.jpg'
        cv2.imwrite(frame_path, frame)
        text += get_text_from_frame(frame_path) + ". "
        os.remove(frame_path)

    print(text)
    text = traslator.translate(text=text, src="en", dest="ru")

    return text

if __name__ == "__main__":
    print(get_text_from_video('00efa58930724f2ae6f9916f53cda3b3.mp4'))
