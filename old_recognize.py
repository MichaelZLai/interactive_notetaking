"""
Simple Flask application to demonstrate the Google Speech API usage.
Install the requirements first:
`pip install SpeechRecognition flask`
Then just run this file, go to http://127.0.0.1:5000/
and upload an audio (or may be even video) file there, using the html form.
(I've tested it with a .wav file only - relying on Google here).
"""

import os
from flask import Flask, request, redirect, flash
from werkzeug.utils import secure_filename

import speech_recognition as sr

app = Flask(__name__)
UPLOAD_FOLDER = "./"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# You have 50 free calls per day, after that you have to register somewhere
# around here probably https://cloud.google.com/speech-to-text/
GOOGLE_SPEECH_API_KEY = 'AIzaSyBflRBGDj8MpUmnLLIZATI2_HyCQg9L-gY'


@app.route("/", methods=["GET", "POST"])
def index():
    extra_line = ''
    if request.method == "POST":
        # Check if the post request has the file part.
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If user does not select file, browser also
        # submit an empty part without filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            # Speech Recognition stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            text = recognizer.recognize_google(
                audio_data, key=GOOGLE_SPEECH_API_KEY, language="ru-RU"
            )
            extra_line = f'Your text: "{text}"'

            # Saving the file.
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            extra_line += f"<br>File saved to {filepath}"

    return f"""
    <!doctype html>
    <title>Upload new File</title>
    {extra_line}
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <p/>
      <input type=submit value=Upload>
    </form>
    """


if __name__ == "__main__":
    app.run(debug=True, threaded=True)