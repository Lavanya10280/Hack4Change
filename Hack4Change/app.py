import streamlit as st
from translate import Translator
from gtts import gTTS
import pytesseract
import cv2
from PIL import Image
import numpy as np
import os

# Initialize Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ensure tesseract is installed and configured

def extract_text(image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(image)
    return text

def translate_text_chunk(text, target_language='ta'):
    translator = Translator(to_lang=target_language)
    translated = translator.translate(text)
    return translated

def translate_text(text, target_language='ta', chunk_size=500):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = [translate_text_chunk(chunk, target_language) for chunk in chunks]
    translated_text = " ".join(translated_chunks)
    return translated_text

def text_to_speech(text, lang='ta'):
    tts = gTTS(text=text, lang=lang)
    audio_path = "output.mp3"
    tts.save(audio_path)
    return audio_path

def save_text_as_pdf(text, filename="translated_text.pdf"):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    font_path = "Latha.ttf"  # Ensure this path is correct
    pdf.add_font("Latha", "", font_path, uni=True)
    pdf.set_font("Latha", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename, 'F')

def main():
    st.title("Image Text Extractor, Translator, and TTS")
    
    # Image upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        
        if st.button("Process"):
            # Extract text from image
            extracted_text = extract_text(image)
            st.write("**Extracted Text:**")
            st.write(extracted_text)

            # Translate the extracted text
            translated_text = translate_text(extracted_text, target_language='ta')
            st.write("**Translated Text:**")
            st.write(translated_text)

            # Convert translated text to speech
            audio_file = text_to_speech(translated_text, lang='ta')
            st.audio(audio_file)

            # Save translated text as PDF
            save_text_as_pdf(translated_text)
            st.success("Translated text saved as PDF.")
            with open("translated_text.pdf", "rb") as pdf_file:
                st.download_button("Download PDF", data=pdf_file, file_name="translated_text.pdf", mime="application/pdf")

if __name__ == '__main__':
    main()

