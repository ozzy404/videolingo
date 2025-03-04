import os
import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip
import whisper

def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, logger=None)
    clip.close()

def transcribe_audio(audio_path, language):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language=language)
    return result["text"]

def translate_text(text, target_lang):
    # Зразкова реалізація перекладу.
    translated_text = f"[Перекладено на {target_lang}]: " + text
    return translated_text

def clone_voice(original_audio_path, translated_text, output_audio_path, target_lang="en"):
    """
    Викликає локальний модуль голосового клонування (наприклад, GPT-SoVITS TTS),
    який аналізує оригінальне аудіо та синтезує нове аудіо, що озвучує translated_text,
    зберігаючи голосові характеристики оригіналу.
    """
    try:
        from core.all_tts_functions.gpt_sovits_tts import synthesize_voice
    except ImportError:
        raise RuntimeError(
            "Модуль голосового клонування GPT-SoVITS TTS не знайдено. "
            "Переконайтеся, що файл core/all_tts_functions/gpt_sovits_tts.py існує та налаштовано коректно."
        )
    # Викликаємо функцію для синтезу дубльованого аудіо.
    synthesize_voice(original_audio_path, translated_text, output_audio_path)

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
    # Вихідний аудіофайл можна зберігати як .wav або інший формат, що підтримує ваш модуль.
    dubbed_audio_path = os.path.join(temp_dir, "dubbed_audio.wav")
    output_video_path = os.path.join(temp_dir, "dubbed_video.mp4")

    # 1. Витягуємо аудіо з відео
    extract_audio(video_path, audio_path)
    
    # 2. Транскрибуємо аудіо за допомогою Whisper
    transcription = transcribe_audio(audio_path, orig_lang)
    print("Транскрипція:", transcription)
    
    # 3. Перекладаємо текст
    translated_text = translate_text(transcription, target_lang)
    print("Перекладений текст:", translated_text)
    
    # 4. Генеруємо аудіо із клонуванням голосу (використовуємо модуль GPT-SoVITS TTS)
    clone_voice(audio_path, translated_text, dubbed_audio_path, target_lang)
    
    # 5. Зливаємо нове аудіо з оригінальним відео
    merge_audio_video(video_path, dubbed_audio_path, output_video_path)

    return output_video_path
