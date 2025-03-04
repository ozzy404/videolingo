import gradio as gr
from processing import process_video

def gradio_interface(video, source_lang, target_lang):
    video_output, translated_text = process_video(video, source_lang, target_lang)
    return video_output, translated_text

iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Video(label="Завантажте відео"),
        gr.Dropdown(choices=["en", "ru", "fr", "de", "it", "es", "ja", "zh"],
                    label="Мова оригіналу", value="en"),
        gr.Dropdown(choices=["en", "ru", "fr", "de", "it", "es", "ja", "zh"],
                    label="Цільова мова", value="ru")
    ],
    outputs=[
        gr.Video(label="Дубльоване відео"),
        gr.Textbox(label="Перекладений текст")
    ],
    title="Перекладач відео та клонування голосу",
    description="Цей інструмент перекладає те, що сказано у відео, на іншу мову та намагається клонувати оригінальний голос."
)

if __name__ == "__main__":
    iface.launch()
