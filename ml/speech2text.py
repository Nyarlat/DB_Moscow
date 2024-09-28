import whisper
import os
import ffmpeg


def extract_audio_from_video(video_path, audio_path):
    """Extract audio from a video file and save it to a specified path."""
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
    """Trim the audio file to a maximum duration."""
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
