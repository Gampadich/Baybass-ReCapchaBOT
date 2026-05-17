import os
import time
from pydub import AudioSegment
import speech_recognition as sr

def transcribe_audio(mp3_path='captcha_audio.mp3'):
    wav_path = "temp_captcha_audio.wav"
    try:
        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format="wav")

        recognizer = sr.Recognizer()

        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)

        text_result = recognizer.recognize_google(audio_data, language='en-US')

        del audio_data
        del source

        return text_result

    except Exception as e:
        print(e)
        if os.path.exists(wav_path):
            os.remove(wav_path)
        return None

    finally:
        if os.path.exists(wav_path):
            try:
                time.sleep(0.1)
                os.remove(wav_path)
            except Exception as clear_error:
                print(f"Не вдалося видалити тимчасовий файл: {clear_error}")
