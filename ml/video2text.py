import cv2
import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to("cuda")


def calculate_histogram(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
    return hist


def extract_frames(video_path, frames_to_extract=10, similarity_threshold=0.9):
    # Открываем видео файл
    cap = cv2.VideoCapture(video_path)

    # Получаем общее количество кадров и частоту кадров
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Общее количество кадров: {total_frames}")

    # Извлекаем все кадры и их гистограммы
    all_frames = []
    all_histograms = []

    for i in range(total_frames):
        ret, frame = cap.read()
        if ret:
            all_frames.append(frame)
            all_histograms.append(calculate_histogram(frame))
        else:
            print(f"Не удалось прочитать кадр {i + 1}")

    cap.release()

    # Фильтруем похожие кадры
    unique_frames = []
    unique_histograms = []

    for i in range(len(all_histograms)):
        current_hist = all_histograms[i]

        # Проверка на похожесть с предыдущими уникальными кадрами
        is_similar = False
        for hist in unique_histograms:
            similarity = cv2.compareHist(hist, current_hist, cv2.HISTCMP_CORREL)
            if similarity > similarity_threshold:
                is_similar = True
                break

        if not is_similar:
            unique_frames.append(all_frames[i])
            unique_histograms.append(current_hist)

    print(f"Уникальные кадры: {len(unique_frames)}")

    # если кадров меньше 10 то берем их
    if len(unique_frames) < 10:
        return unique_frames

    # прежняя логика выделения кадров через интервал
    interval = len(unique_frames) // frames_to_extract
    extracted_frames = [unique_frames[i] for i in range(0, len(unique_frames), interval)][:frames_to_extract]

    print(f"Извлечено уникальных кадров: {len(extracted_frames)}")
    print(extracted_frames)
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

    return text


if __name__ == "__main__":
    #print(get_text_from_video('00efa58930724f2ae6f9916f53cda3b3.mp4'))
    extract_frames("35test_vid.mp4")

