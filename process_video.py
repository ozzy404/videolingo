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
    """
    Використовує argostranslate для перекладу тексту.
    Якщо target_lang == "en", припускаємо, що вхідний текст російською,
    і виконуємо переклад з російської на англійську.
    Для інших мов наразі повертаємо шаблонний рядок.
    """
    try:
        import argostranslate.translate as translate
    except ImportError:
        raise RuntimeError("argostranslate не встановлено. Додайте його до requirements.txt.")
    
    installed_languages = translate.get_installed_languages()
    from_lang = None
    to_lang = None

    if target_lang == "en":
        for lang in installed_languages:
            if lang.code == "ru":
                from_lang = lang
            if lang.code == "en":
                to_lang = lang
    else:
        # Якщо цільова мова не англійська – поки що повертаємо зразковий рядок.
        return f"[Перекладено на {target_lang}]: " + text

    if from_lang is None or to_lang is None:
        raise RuntimeError("Не знайдено необхідні мовні пакети для перекладу. Завантажте їх через argostranslate.")

    translation = from_lang.get_translation(to_lang)
    translated_text = translation.translate(text)
    return translated_text

def clone_voice(original_audio_path, translated_text, output_audio_path, target_lang="en"):
    """
    Викликає локальний модуль голосового клонування (наприклад, GPT-SoVITS TTS),
    який аналізує оригінальне аудіо та синтезує нове аудіо із збереженням голосових характеристик.
    """
    try:
        from core.all_tts_functions.gpt_sovits_tts import synthesize_voice
    except ImportError:
        raise RuntimeError(
            "Модуль голосового клонування GPT-SoVITS TTS не знайдено. "
            "Переконайтеся, що файл core/all_tts_functions/gpt_sovits_tts.py існує та налаштовано."
        )
    synthesize_voice(original_audio_path, translated_text, output_audio_path)

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
    dubbed_audio_path = os.path.join(temp_dir, "dubbed_audio.wav")
    output_video_path = os.path.join(temp_dir, "dubbed_video.mp4")

    extract_audio(video_path, audio_path)
    transcription = transcribe_audio(audio_path, orig_lang)
    print("Транскрипція:", transcription)
    translated_text = translate_text(transcription, target_lang)
    print("Перекладений текст:", translated_text)
    clone_voice(audio_path, translated_text, dubbed_audio_path, target_lang)
    merge_audio_video(video_path, dubbed_audio_path, output_video_path)
    return output_video_path
