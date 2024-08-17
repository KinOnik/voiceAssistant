import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print(f"Вы сказали: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Не удалось распознать речь.")
        return ""
    except sr.RequestError:
        print("Ошибка при обращении к сервису.")
        return ""
