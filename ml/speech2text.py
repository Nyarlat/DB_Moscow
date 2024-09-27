import whisper
import os
from moviepy.editor import VideoFileClip


def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path, fps=16000, nbytes=2, codec='pcm_s16le', bitrate="16k")


def speech_recognition(video_path, model='base'):
    audio_path = "audio.wav"
    speech_model = whisper.load_model(model, device="cuda")
    extract_audio_from_video(video_path, audio_path)
    result = speech_model.transcribe(audio_path)

    # Удаляем файл аудиодорожки
    os.remove(audio_path)

    return result['text']
