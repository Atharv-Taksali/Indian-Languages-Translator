import os
import tkinter as tk #GUI
from tkinter import messagebox
import speech_recognition as sr #Audio I/O
from googletrans import Translator #Translation
from gtts import gTTS
import pygame #Audio playback

#Language Codes
LANGUAGES = {
    "1. English": "en",
    "2. Hindi": "hi",
    "3. Bengali": "bn",
    "4. Marathi": "mr",
    "5. Telugu": "te",
    "6. Tamil": "ta",
    "7. Gujarati": "gu",
    "8. Urdu": "ur",
    "9. Kannada": "kn",
    "10. Odia": "or",
    "11. Malayalam": "ml",
    "12. Punjabi": "pa",
}

#Listen for audio input, handle exceptions and return translated text
def listen_for_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            status_label.config(text="Listening... Please speak.") 
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            status_label.config(text=f"You said: {text}")
            return text
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            messagebox.showerror("Error", "Speech recognition service unavailable.")
            return None

#Convert translated text to audio file
def speak_text_gtts(translated_text, lang='hi'):
    tts = gTTS(translated_text, lang=lang)
    temp_file_path = "temp_audio.mp3"
    tts.save(temp_file_path)
    return temp_file_path


#Play audio file
def play_audio_file(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    # Stop and unload the mixer after playback
    pygame.mixer.music.unload()

#Translate audio input
def translateAudio():
    source_lang = source_lang_entry.get().strip()
    target_lang = target_lang_entry.get().strip()

    if not source_lang or not target_lang:
        messagebox.showwarning("Warning", "Please enter both source and target language codes.")
        return

    status_label.config(text="Speak Now...", fg="green")

    root.after(1000, start_listening, source_lang, target_lang)

#Start listening for audio input (ensures "Speak Now" is visible)
def start_listening(source_lang, target_lang):
    source_text = listen_for_input()
    if source_text:
        translator = Translator()
        translated = translator.translate(source_text, src=source_lang, dest=target_lang).text
        status_label.config(text=f"Translated: {translated}")
        file_path = speak_text_gtts(translated, lang=target_lang)
        try:
            play_audio_file(file_path)
        finally:
            # Clean up temporary audio file
            if os.path.exists(file_path):
                os.remove(file_path)
    else:
        status_label.config(text="No input detected. Please try again.", fg="red")



# Initialise Tkinter
root = tk.Tk()
root.title("Indian Languages Voice Translator")
root.geometry("500x500")

# Display available languages
tk.Label(root, text = "Available Languages:", font = ("Arial", 12, "bold")).pack(pady = 5)
languages_text = "\n".join([f"{key} ({code})" for key, code in LANGUAGES.items()])
tk.Label(root, text = languages_text, justify = "left").pack(pady = 5)

# Input language codes
tk.Label(root, text = "Source Language Code (e.g., 'en')").pack(pady = 5)
source_lang_entry = tk.Entry(root, width = 20)
source_lang_entry.pack(pady = 5)

tk.Label(root, text = "Target Language Code (e.g., 'hi')").pack(pady = 5)
target_lang_entry = tk.Entry(root, width = 20)
target_lang_entry.pack(pady = 5)

# Translate button
translate_button = tk.Button(root, text = "Translate", command = translateAudio, bg = "green", fg = "white")
translate_button.pack(pady = 20)

# Status
status_label = tk.Label(root, text = "", fg = "blue")
status_label.pack(pady = 10)

# Start the Tkinter event loop
root.mainloop()