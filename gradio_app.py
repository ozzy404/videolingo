import gradio as gr
import os
import shutil
from core.config_utils import update_key
from core.step2_whisperX import transcribe
# Інші імпорти для обробки (за потребою)
# from core.step3_1_spacy_split import split_by_spacy
# from core.step3_2_splitbymeaning import split_sentences_by_meaning
# from core.step4_1_summarize import get_summary
# from core.step4_2_translate_all import translate_all
# from core.step5_splitforsub import split_for_sub_main
# from core.step6_generate_final_timeline import align_timestamp_main
# from core.step7_merge_sub_to_vid import merge_subtitles_to_video
# from core.step8_1_gen_audio_task import gen_audio_task_main
# from core.step8_2_gen_dub_chunks import gen_dub_chunks
# from core.step9_extract_refer_audio import extract_refer_audio_main
# from core.step10_gen_audio import gen_audio
# from core.step11_merge_full_audio import merge_full_audio
# from core.step12_merge_dub_to_vid import merge_video_audio

def process_video(video_path, source_language, target_language):
    # Опціонально: видаляємо всі існуючі відеофайли (щоб find_video_files() точно знаходив лише один файл)
    allowed_exts = [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"]
    for file in os.listdir("."):
        if any(file.lower().endswith(ext) for ext in allowed_exts):
            try:
                os.remove(file)
            except Exception as e:
                print(f"Не вдалося видалити {file}: {e}")
    
    # Копіюємо завантажений файл у поточну директорію з фіксованим ім'ям
    dest_path = "input_video.mp4"
    shutil.copy(video_path, dest_path)
    
    # Оновлюємо конфігурацію для мови транскрипції та перекладу
    update_key("whisper.language", source_language)
    update_key("target_language", target_language)
    
    # Викликаємо транскрипцію. Функція transcribe() шукає відеофайли у поточній директорії,
    # тому зараз вона повинна знайти "input_video.mp4"
    transcript = transcribe()
    
    # Далі мають виконуватись інші етапи обробки (розбиття, переклад, генерація субтитрів, дубляж аудіо)
    # Для прикладу, залишаємо заглушку:
    processed_video = "output/output_dub.mp4"
    subtitles = "output/subtitles.srt"
    return processed_video, subtitles

iface = gr.Interface(
    fn=process_video,
    inputs=[
        gr.Video(label="Завантажте відео", type="filepath"),
        gr.Dropdown(choices=["en", "zh", "ru", "fr", "de", "it", "es", "ja"], label="Мова оригіналу"),
        gr.Dropdown(choices=["en", "zh", "ru", "fr", "de", "it", "es", "ja"], label="Мова перекладу")
    ],
    outputs=[
        gr.Video(label="Відео з дубляжем"),
        gr.Textbox(label="Субтитри")
    ],
    title="VideoLingo Gradio"
)

if __name__ == "__main__":
    # share=True видасть публічне посилання, яке з’явиться у виводі Colab
    iface.launch(share=True)
