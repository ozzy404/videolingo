import os
import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip
import whisper

def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, logger=None)
    clip.close()

def transcribe_audio(audio_path, language):
    # Завантаження моделі Whisper – можна використовувати "base" для швидкості або інший варіант
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language=language)
    return result["text"]

def translate_text(text, target_lang):
    # Тут можна інтегрувати офлайн‑перекладач (наприклад, argos‑translate)
    # Для демонстрації просто повертаємо текст з приміткою
    translated_text = f"[Перекладено на {target_lang}]: " + text
    return translated_text

def clone_voice(original_audio_path, translated_text, output_audio_path):
    # Шаблонна реалізація для озвучення тексту – НЕ клонування голосу
    # Замість pyttsx3 інтегруйте локальний алгоритм клонування голосу (наприклад, RVC‑алгоритм)
    import pyttsx3
    engine = pyttsx3.init()
    engine.save_to_file(translated_text, output_audio_path)
    engine.runAndWait()

def merge_audio_video(video_path, new_audio_path, output_video_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(new_audio_path)
    final_video = video.set_audio(audio)
    final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac", logger=None)
    video.close()
    audio.close()

def process_video_dub(video_path, orig_lang, target_lang):
    # Створення тимчасової директорії для обробки
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, "original_audio.wav")
    dubbed_audio_path = os.path.join(temp_dir, "dubbed_audio.wav")
    output_video_path = os.path.join(temp_dir, "dubbed_video.mp4")

    # 1. Виділення аудіо з відео
    extract_audio(video_path, audio_path)

    # 2. Транскрипція аудіо за допомогою Whisper
    transcription = transcribe_audio(audio_path, orig_lang)
    print("Транскрипція:", transcription)

    # 3. Переклад тексту
    translated_text = translate_text(transcription, target_lang)
    print("Перекладений текст:", translated_text)

    # 4. Генерація нового аудіо із клонуванням голосу
    clone_voice(audio_path, translated_text, dubbed_audio_path)

    # 5. Об’єднання нового аудіо з оригінальним відео
    merge_audio_video(video_path, dubbed_audio_path, output_video_path)

    return output_video_path
