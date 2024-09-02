import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import random
import os
import speech_recognition as sr
from gtts import gTTS

# Function to load responses from files
def load_responses(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

# Load responses
responses = load_responses('Text.txt')
responses2 = load_responses('Text2.txt')
responses3 = load_responses('Text3.txt')
responses4 = load_responses('Text4.txt')
responses5 = load_responses('Text5.txt')
responses6 = load_responses('Text6.txt')

all_responses = [responses, responses2, responses3, responses4, responses5, responses6]
keywords = ['กิน', 'ทาน', 'หิว']
keywords2 = ['คุณคือใคร', 'เธอเป็นใคร', 'เธอ']
keywords3 = ['เที่ยว', 'เบื่อ', 'ไปไหน']
keywords4 = ['หนัง', 'แนะนำหนัง', 'ดูหนัง', 'ดูอะไรดี']
keywords5 = ['เรื่องราว', 'เล่า', 'บอก', 'พูด']
keywords6 = ['มีไรให้ช่วย', 'ช่วยด้วย', 'ช่วย']
all_keywords = [keywords, keywords2, keywords3, keywords4, keywords5, keywords6]

error_responses = ["ฉันไม่เข้าใจ", "พูดอีกทีได้ไหม", "คุณว่ายังไงนะ"]
request_error_responses = ["ฉันไม่เข้าใจ", "ฉันไม่รู้", "ฉันตอบไม่ได้"]

# Function to check for keywords and generate a response
def generate_response(text):
    for key_list, resp_list in zip(all_keywords, all_responses):
        for keyword in key_list:
            if keyword in text:
                return random.choice(resp_list)
    return None

# Function to handle speech recognition and responses
def handle_speech():
    input_text = speech_to_text()
    if input_text:
        response = generate_response(input_text)
        if response:
            save_response(response)
        else:
            print("Bot: No relevant keywords found.")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="th")
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("ฉันไม่เข้าใจ")
        return "ฉันไม่เข้าใจ"
    except sr.RequestError as e:
        print(f"ฉันไม่เข้าใจ; {e}")
        return "Sorry, I couldn't request results."

def save_response(response):
    tts = gTTS(text=response, lang='th')
    output_dir = 'output2'
    os.makedirs(output_dir, exist_ok=True)
    wav_path = os.path.join(output_dir, 'response.wav')
    tts.save(wav_path)

# Setting up the GUI
root = tk.Tk()
root.title("Speech Recognition Bot")

chat_window = scrolledtext.ScrolledText(root, state='disabled', width=60, height=10)
chat_window.grid(row=0, column=0, columnspan=2)

run_button = tk.Button(root, text="Run", command=lambda: Thread(target=handle_speech).start())
run_button.grid(row=1, column=0, pady=10)

quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.grid(row=1, column=1, pady=10)

root.mainloop()
