import webbrowser as wb
import speech_recognition as sr

# Establishes different recognizers
r1 = sr.Recognizer()
r2 = sr.Recognizer()
r3 = sr.Recognizer()

# Opens microphone and records audio
with sr.Microphone() as source:
    print('say video')
    audio = r3.listen(source)


if 'video' in r1.recognize_google(audio):
    r1 = sr.Recognizer()
    url = 'https://www.youtube.com/results?search_query='
    with sr.Microphone() as source:
        print('What do you want to search on youtube?')
        audio = r1.listen(source)

        try:
            get = r1.recognize_google(audio)
            print(get)
            wb.get().open_new(url+get)
        except sr.UnknownValueError:
            print('could not understand')
        except sr.RequestError as e:
            print(e)
        
