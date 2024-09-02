import tkinter as tk
from tkinter import messagebox
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import pygame
import mutagen.mp3
import os

class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")
        self.root.geometry("1080x720")

        self.label = tk.Label(root, text="Press the button to start listening")
        self.label.pack(pady=20)

        self.button = tk.Button(root, text="Start Listening", command=self.start_listening)
        self.button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.pack(pady=10)

        self.canvas = tk.Canvas(root, width=720, height=1080)
        self.canvas.pack()

        self.video_thread = None
        self.video_running = False

        # Initialize pygame for audio playback
        pygame.mixer.init()

        # Updated Mapping phrases to video files
        self.phrase_to_video = {
            "น้ำตาล": "1.mp4",  # "น้ำตาล" will trigger playing "1.mp4"
            "เกลือ": "2.mp4",   # "เกลือ" will trigger playing "2.mp4"
            "ห้องน้ำ": "3.mp4",  # "ห้องน้ำ" will trigger playing "3.mp4"
            "สมัครสมาชิก": "4.mp4"  # "สมัครสมาชิก" will trigger playing "4.mp4"
        }

    def play_audio(self, audio_path, callback=None):
        if os.path.isfile(audio_path):
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            if callback:
                # Schedule the callback to be called after the audio finishes
                audio_length = self.get_audio_length(audio_path)
                self.root.after(int(audio_length * 1000), callback)  # Convert to milliseconds and ensure integer
        else:
            print(f"Error: No file '{audio_path}' found.")
            self.label.config(text=f"No audio file '{audio_path}' found.")

    def get_audio_length(self, audio_path):
        # This function will estimate the length of the audio in seconds.
        audio = mutagen.mp3.MP3(audio_path)
        return audio.info.length

    def play_video(self, video_path):
        self.video_running = True
        self.video_clip = VideoFileClip(video_path)
        self.video_clip.preview()  # Play video with synchronized audio

    def play_video_and_then_callback(self, video_path, callback=None):
        self.video_running = True
        self.video_clip = VideoFileClip(video_path)
        self.video_clip.preview()  # Play video with synchronized audio

        # Schedule the callback to be called after the video finishes
        video_length = self.video_clip.duration
        self.root.after(int(video_length * 1000), callback)  # Convert to milliseconds and ensure integer

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
            # Check if the recognized text contains one of the phrases in the dictionary
            video_to_play = None
            for phrase, video in self.phrase_to_video.items():
                if phrase in text:
                    video_to_play = video
                    break
            if video_to_play:
                self.play_video_and_then_callback(video_to_play, lambda: self.play_audio("aging1.mp3"))
            else:
                self.label.config(text="Phrase not recognized or not mapped to a video.")
                self.play_audio('no.mp3')  # Play 'no.mp3' on error
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            self.label.config(text="Could not understand the audio.")
            self.play_audio('no.mp3')  # Play 'no.mp3' on error
        except sr.RequestError:
            print("Sorry, there was an error with the speech recognition service.")
            self.label.config(text="Error with the speech recognition service.")
            self.play_audio('no.mp3')  # Play 'no.mp3' on error

    def start_listening(self):
        if self.video_thread is None or not self.video_thread.is_alive():
            # Play the video file before starting speech recognition without delay
            self.play_video_and_then_callback('hello.mp4', self.listen_for_phrase)
        else:
            messagebox.showinfo("Info", "Already listening")

    def exit_app(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.mainloop()
