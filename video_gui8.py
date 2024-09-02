import tkinter as tk
from tkinter import messagebox
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import pygame
import mutagen.mp3
import os
import webbrowser  # Import the webbrowser module

class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")
        self.root.geometry("1080x720")

        self.label = tk.Label(root, text="Press the button to start listening")
        self.label.pack(pady=20)

        self.button = tk.Button(root, text="Start Listening", command=self.start_listening)
        self.button.pack(pady=10)

        self.canvas = tk.Canvas(root, width=720, height=1080)
        self.canvas.pack()

        self.video_thread = None
        self.video_running = False

        pygame.mixer.init()

        self.phrase_to_video = {
            "น้ำตาล": "1.mp4",
            "เกลือ": "2.mp4",
            "ห้องน้ำ": "3.mp4",
            "สมัครสมาชิก": "4.mp4"
        }

    def play_audio(self, audio_path, callback=None):
        if os.path.isfile(audio_path):
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            if callback:
                audio_length = self.get_audio_length(audio_path)
                self.root.after(int(audio_length * 1000), callback)
        else:
            print(f"Error: No file '{audio_path}' found.")
            self.label.config(text=f"No audio file '{audio_path}' found.")

    def get_audio_length(self, audio_path):
        audio = mutagen.mp3.MP3(audio_path)
        return audio.info.length

    def play_video(self, video_path):
        self.video_running = True
        self.video_clip = VideoFileClip(video_path)
        self.video_clip.preview()

    def play_video_and_then_callback(self, video_path, callback=None):
        self.video_running = True
        self.video_clip = VideoFileClip(video_path)
        self.video_clip.preview()

        video_length = self.video_clip.duration
        self.root.after(int(video_length * 1000), callback)

    def listen_for_phrase(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            print("Listening for phrases...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio, language='th-TH')
            print(f"Heard: {text}")
            video_to_play = None
            for phrase, video in self.phrase_to_video.items():
                if phrase in text:
                    video_to_play = video
                    break

            if "น้ำตาล" in text:
                webbrowser.open("index.html")  # Open index.html when "น้ำตาล" is recognized
            elif video_to_play:
                self.play_video_and_then_callback(video_to_play, lambda: self.play_video("Q.mp4"))
            else:
                self.label.config(text="Phrase not recognized or not mapped to a video.")
                self.play_video('no.mp4')
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            self.label.config(text="Could not understand the audio.")
            self.play_video('no.mp4')
        except sr.RequestError:
            print("Sorry, there was an error with the speech recognition service.")
            self.label.config(text="Error with the speech recognition service.")
            self.play_video('no.mp4')

    def start_listening(self):
        if self.video_thread is None or not self.video_thread.is_alive():
            self.play_video_and_then_callback('hello.mp4', self.listen_for_phrase)
        else:
            messagebox.showinfo("Info", "Already listening")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.mainloop()
