import gradio as gr
from process_video import process_video_dub

def process_video(video, orig_lang, target_lang):
    if video is None:
        return "Не завантажено відео"
    # process_video_dub очікує шлях до файлу (Gradio зберігає завантажене відео у тимчасовому файлі)
    output_video_path = process_video_dub(video, orig_lang, target_lang)
    return output_video_path

iface = gr.Interface(
    fn=process_video,
    inputs=[
        gr.Video(label="Завантажте відео"),
        gr.Dropdown(choices=["en", "ru", "fr", "de", "it", "es", "ja", "zh"],
                    label="Мова оригіналу"),
        gr.Dropdown(choices=["en", "ru", "fr", "de", "it", "es", "ja", "zh"],
                    label="Мова перекладу")
    ],
    outputs=gr.Video(label="Дубльоване відео"),
    title="Переклад та дубляж відео",
    description="Завантажте відео, виберіть мову оригіналу та мову перекладу. Система спочатку транскрибує аудіо, потім перекладає текст і, використовуючи локальний алгоритм голосового клонування, генерує нове аудіо, яке зливається з відео."
)

if __name__ == "__main__":
    iface.launch(share=True)
