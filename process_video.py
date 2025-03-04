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
    # Зразкова реалізація перекладу. Тут можна інтегрувати офлайн-перекладач.
    translated_text = f"[Перекладено на {target_lang}]: " + text
    return translated_text

def clone_voice(original_audio_path, translated_text, output_audio_path, target_lang="en"):
    # Використовуємо gTTS для генерації аудіо.
    try:
        from gtts import gTTS
    except ImportError:
        raise RuntimeError("Модуль gTTS не встановлено. Додайте його до requirements.txt")
    # Маппінг мов для gTTS (для 'zh' використовуємо 'zh-cn')
    gtts_lang_map = {
        "en": "en",
        "ru": "ru",
        "fr": "fr",
        "de": "de",
        "it": "it",
        "es": "es",
        "ja": "ja",
        "zh": "zh-cn"
    }
    lang = gtts_lang_map.get(target_lang, "en")
    tts = gTTS(text=translated_text, lang=lang)
    tts.save(output_audio_path)

def merge_audio_video(video_path, new_audio_path, output_video_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(new_audio_path)
    final_video = video.set_audio(audio)
    final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac", logger=None)
    video.close()
    audio.close()

def process_video_dub(video_path, orig_lang, target_lang):
    # Створюємо тимчасову директорію для обробки
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, "original_audio.wav")
    # gTTS генерує mp3 файл – тому розширення .mp3
    dubbed_audio_path = os.path.join(temp_dir, "dubbed_audio.mp3")
    output_video_path = os.path.join(temp_dir, "dubbed_video.mp4")

    # 1. Витягуємо аудіо з відео
    extract_audio(video_path, audio_path)
    
    # 2. Транскрибуємо аудіо за допомогою Whisper
    transcription = transcribe_audio(audio_path, orig_lang)
    print("Транскрипція:", transcription)
    
    # 3. Перекладаємо текст
    translated_text = translate_text(transcription, target_lang)
    print("Перекладений текст:", translated_text)
    
    # 4. Генеруємо аудіо через gTTS (зразок синтезу голосу)
    clone_voice(audio_path, translated_text, dubbed_audio_path, target_lang)
    
    # 5. Зливаємо нове аудіо з оригінальним відео
    merge_audio_video(video_path, dubbed_audio_path, output_video_path)

    return output_video_path
