import pyaudio
import speech_recognition as sr

def list_microphones():
    """
    List all available microphone devices.
    """
    print("Available Microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index}: {name}")

def recognize_speech_from_mic(recognizer, microphone, language_code='en-US'):
    """
    Capture and recognize speech from the microphone.
    :param recognizer: An instance of sr.Recognizer
    :param microphone: An instance of sr.Microphone
    :param language_code: Language code for recognition (default is 'en-US')
    """
    with microphone as source:
        print("Listening...")
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language=language_code)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

if __name__ == "__main__":
    # Initialize recognizer and microphone
    recognizer = sr.Recognizer()
    list_microphones()
    
    # Use the second microphone in the list as an example (index 1)
    mic_index = 1
    microphone = sr.Microphone(device_index=mic_index)

    # Specify the language code you want to use
    language_code = 'th'  # Change this to your desired language code

    print("Press Ctrl+C to stop.")
    try:
        while True:
            result = recognize_speech_from_mic(recognizer, microphone, language_code)
            if result["transcription"]:
                print("You said:", result["transcription"])
            if not result["success"]:
                print("I didn't catch that. What did you say?\n")
            if result["error"]:
                print("ERROR:", result["error"])
    except KeyboardInterrupt:
        print("\nExiting...")


# English (US): 'en-US'
# English (UK): 'en-GB'
# Spanish: 'es-ES'
# French: 'fr-FR'
# German: 'de-DE'
# Chinese (Simplified): 'zh-CN'
# Japanese: 'ja-JP'
# Korean: 'ko-KR'
# Portuguese (Brazil): 'pt-BR'
# Russian: 'ru-RU'
# Italian: 'it-IT'
# Thai: 'th'
# Arabic (Egypt): 'ar-EG'
# Hindi: 'hi-IN'