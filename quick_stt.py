import speech_recognition as sr

r = sr.Recognizer()

# Define audio file
audio = 'peacock.wav'

# Process the audio file speech to text
with sr.AudioFile(audio) as source:
    audio = r.record(source)
    print('Done')

try:
    text = r.recognize_google_cloud(audio)
    print(text)

except Exception as e:
    print(e)