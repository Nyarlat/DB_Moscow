import whisper
import os
from moviepy.editor import VideoFileClip, AudioFileClip


def extract_audio_from_video(video_path, audio_path):
    """Extract audio from a video file and save it to a specified path."""
    try:
        with VideoFileClip(video_path) as video:
            audio = video.audio
            audio.write_audiofile(audio_path, fps=16000, nbytes=2, codec='pcm_s16le', bitrate="16k")
    except Exception as e:
        print(f"Error extracting audio: {e}")


def trim_audio(audio_path, max_duration=600):
    """Trim the audio file to a maximum duration."""
    try:
        with AudioFileClip(audio_path) as audio:
            if audio.duration > max_duration:
                trimmed_audio = audio.subclip(0, max_duration)
                trimmed_audio.write_audiofile(audio_path, fps=16000, nbytes=2, codec='pcm_s16le', bitrate="16k")
    except Exception as e:
        print(f"Error trimming audio: {e}")


def speech_recognition(video_path, model='base'):
    """Perform speech recognition on the audio extracted from the video."""
    audio_path = "audio.wav"

    # Load the Whisper model
    speech_model = whisper.load_model(model, device="cuda")

    # Extract and trim audio
    extract_audio_from_video(video_path, audio_path)
    trim_audio(audio_path)

    # Transcribe the trimmed audio
    try:
        result = speech_model.transcribe(audio_path, language='ru')
        print(result)
        return result['text']
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
    finally:
        # Clean up the temporary audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)


if __name__ == "__main__":
    print(speech_recognition('9007f33c8347924ffa12f922da2a179d.mp4'))
