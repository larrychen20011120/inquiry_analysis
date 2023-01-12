import time
from pydub import AudioSegment
import os
import socket
import sys
import struct
import time
import json

import pyimgur
import librosa
import soundfile as sf
from pyannote.audio import Pipeline
from wordcloud import WordCloud
import azure.cognitiveservices.speech as speechsdk

from app import app, db
from app.model import Task, File, AnalysisResult

# NER API (WMMKS LAB)
HOST, PORT = "140.116.245.151", 9995
# chinese font for drawing wordcloud image
TC_FONT_PATH = app.config["CHINESE_FONT_URL"]
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token=app.config["PYANNOTE_AUDIO_KEY"])

# Azure (Speech Recognitionn)
def from_file(name):
    speech_config = speechsdk.SpeechConfig(subscription=app.config["AZURE_KEY"], region=app.config["AZURE_REGION"])
    speech_config.speech_recognition_language="zh-TW"
    audio_input = speechsdk.AudioConfig(filename=name)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = speech_recognizer.recognize_once_async().get()
    return result.text

# NER API (WMMKS LAB)
def askForService(token,data):
    # HOST, PORT 記得修改

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    received = ""
    try:
        sock.connect((HOST, PORT))
        msg = bytes(token+"@@@"+data, "utf-8")
        msg = struct.pack(">I", len(msg)) + msg
        sock.sendall(msg)

        # 因為是作Async，所以要等到它做完再回傳
        time.sleep(2)

        received = str(sock.recv(81920), "utf-8")
    finally:
        sock.close()
    return received
def process(token,data):
    # 可在此做預處理

    # 送出
    result = askForService(token,data).encode('utf-8').decode("unicode_escape")
    # 可在此做後處理
    return result

# the function will return the image url from imgur
def getImgUrl(url):
    im = pyimgur.Imgur(app.config["IMGUR_KEY"])
    uploaded_image = im.upload_image(url, title=str(int(time.time())))
    dest = uploaded_image.link
    return dest

def getWordCloud(url):
    token = app.config["WMMKS_NER_KEY"]
    collect = dict()
    with open(url, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.rstrip()
            line = line.split(': ')[-1]

            result = dict(json.loads(process(token,line)))

            for item in result['allList']:
                word = item['data']['origtext']
                if word in collect:
                    collect[word][0] += 1
                else:
                    collect[word] = [1, item['data']['cat']]
    if (len(collect.keys()) > 0):
        # at least one word
        wc = WordCloud(background_color="white",max_words=10,relative_scaling=0.5,normalize_plurals=False, font_path=TC_FONT_PATH).generate_from_frequencies(dict(zip(collect.keys(), [value[0] for value in collect.values()])))
        wc.to_file('temp.png')
        return getImgUrl('temp.png')
    else:
        return "Not Found"


while (True):
    print('Server is active!')
    tasks = Task.query.all()
    if len(tasks) != 0:
        print(f"Receive {len(tasks)} tasks")
        for task in tasks:
            file = File.query.filter_by(id=task.fileId).first()
            if not file.completed:
                start_time = time.time()
                result_name = os.path.join( os.path.join(app.config['ENTRY'], "results"), (str(time.time())+'.txt') )
                # change audio file to wav form
                print(file.url)
                m4a = AudioSegment.from_file(file.url)
                m4a.export('change.wav', 'wav')
                # assuming there are 2 speakers
                diarization = pipeline("change.wav", num_speakers=2)
                x, samplerate = librosa.load("change.wav", sr=16000)
                with open(result_name, "w", encoding='utf-8') as f:
                    # write diarization AnalysisResult
                    for turn, _, speaker in diarization.itertracks(yield_label=True):
                        # split each speaker based on the result of diarization
                        y = x[int(turn.start * samplerate): int(turn.end * samplerate)]
                        sf.write("dest_audio.wav", y, samplerate)
                        result = from_file('dest_audio.wav')
                        f.write(f"{speaker}: {result}\n")
                img_url = getWordCloud(result_name)
                print(f"It takes {int(time.time() - start_time)} seconds to process the whole data.")
                # write back to the database
                file.completed = True
                db.session.add(file)
                ar = AnalysisResult(
                    fileId = task.fileId,
                    result_url = result_name,
                    wordcloud_url = img_url
                )
                db.session.add(ar)      # add the analysis result
                db.session.delete(task) # delete the task which is done
                db.session.commit()

    else:
        # at least every 5 seconds query tasks
        print("Server sleeps for 5 seconds.")
        time.sleep(5)
