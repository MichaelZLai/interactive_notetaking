# Importing Libraries
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
from tqdm import tqdm
# from pydub.silence import split_on_silence


# Splits audio file into chunks and applies speech recognition
def silence_based_conversation(path):
    # Open audio stored in local as wav
    song = AudioSegment.from_wav(path)
    print(song)

    # Open file to concatenate and store recognized text
    fh = open("recognized.txt", "w+")

    # Splitting where silence is .5 sec or more to get chunks
    # chunks = split_on_silence(song, min_silence_len = 400, silence_thresh = -30)
    # print(chunks)

    # Splitting to chunks of 15 sec
    chunk_length_ms = 15000
    chunks = make_chunks(song, chunk_length_ms)
    print(chunks)

    # Create directory to store audio chunks.
    try:
        os.mkdir('audio_chunks')
    except(FileExistsError):
        pass

    # Move into directory to store audio files
    os.chdir('audio_chunks')

    i = 0

    # Process each audio chunk & tqdm showing progress bar
    for chunk in tqdm(chunks):
        # Create 0.5 sec silence chunk
        chunk_silent = AudioSegment.silent(duration = 10)

        # Add 0.5 sec silence to beginning and end (so it doesnt seem abruptly sliced)
        audio_chunk = chunk_silent + chunk + chunk_silent

        # Export audio chunk and save it in current directory
        print("--Saving chunk{0}.wav".format(i))

        # Specify bitrate to be 192k
        audio_chunk.export("./chunk{0}.wav".format(i), bitrate='192k', format="wav")

        # Name newly created chunk
        filename = 'chunk'+str(i)+'.wav'

        print("Transcribing chunk "+str(i))

        # Get name of new chunk
        newchunk = filename

        # Create speech recognition object
        r = sr.Recognizer()

        # Recognize the audio chunk
        with sr.AudioFile(newchunk) as source:
            # r.adjust_for_ambient_noise(source)
            # audio_listened = r.listen(source)
            audio_listened = r.record(source)


        try:
            # Convert to text
            rec = r.recognize_google(audio_listened)
            # Write output to file
            fh.write(rec+". ")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("Could not request results. Check internet connection")
        
        i += 1

    os.chdir('..')

if __name__ == '__main__':
    print("Enter audio file name")

    path = 'peacock.wav'    

    silence_based_conversation(path)
