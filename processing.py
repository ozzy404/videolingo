import moviepy.editor as mp
import os
import tempfile
from whisper import load_model
from googletrans import Translator
from gtts import gTTS

def clone_voice(original_audio_path, text, output_audio_path, source_lang, target_lang):
    """
    Функція-шаблон для клонування голосу.
    Наразі використовує gTTS для генерації аудіо на цільовій мові.
    Для реального голосового клонування (як rvc2, але швидше) інтегруйте відповідну модель тут.
    """
    tts = gTTS(text=text, lang=target_lang)
    tts.save(output_audio_path)
    return output_audio_path

def transcribe_audio(audio_path, source_lang):
    model = load_model("base")  # Використовуємо базову модель Whisper для прикладу
    result = model.transcribe(audio_path, language=source_lang)
    return result["text"]

def translate_text(text, target_lang):
    translator = Translator()
    translated = translator.translate(text, dest=target_lang)
    return translated.text

def merge_audio_video(video_path, audio_path, output_path):
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = mp.AudioFileClip(audio_path)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
    return output_path

def process_video(video_file, source_lang, target_lang):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Збереження завантаженого відео у тимчасову теку
        if isinstance(video_file, str):
            video_path = video_file
        else:
            video_path = os.path.join(tmpdir, "input_video.mp4")
            with open(video_path, "wb") as f:
                f.write(video_file.read())
        
        # Вилучення аудіо з відео
        audio_path = os.path.join(tmpdir, "extracted_audio.wav")
        video_clip = mp.VideoFileClip(video_path)
        video_clip.audio.write_audiofile(audio_path, verbose=False, logger=None)

        # Транскрипція аудіо
        transcript = transcribe_audio(audio_path, source_lang)

        # Переклад транскрипції
        translated_text = translate_text(transcript, target_lang)

        # Генерація дубльованого аудіо з клонуванням голосу
        dubbed_audio_path = os.path.join(tmpdir, "dubbed_audio.mp3")
        clone_voice(audio_path, translated_text, dubbed_audio_path, source_lang, target_lang)

        # Об’єднання нового аудіо з оригінальним відео
        output_video_path = os.path.join(tmpdir, "dubbed_video.mp4")
        merge_audio_video(video_path, dubbed_audio_path, output_video_path)

        # Повертаємо шлях до фінального відео та перекладений текст
        return output_video_path, translated_text
