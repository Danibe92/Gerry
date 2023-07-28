import speech_recognition as sr
from tensorflow.keras.models import load_model
from scipy.io.wavfile import write
from pyaudio import paInt16,PyAudio
import atexit
import numpy as np
from sounddevice import rec,wait
from script.all import load,generate_response
from script.blu import connect_to_device
from script.scroccogpt import load_session,pizzagpt
from script.musica import youtube_music,music_driver,skippa,quit
from script.talk import Talk  #comando per la voce di Gerry se la vuoi usare
from pyttsx3 import init
import librosa
import threading
from queue import Queue
from platform import system
username = "DaniBe91"
password = "VivaGerryfake"
tts = Talk(username, password)
driver=load_session("./script/chromedriver.exe")
driverm=music_driver("./script/chromedriver.exe")
fs = 44100
seconds = 2
filename = "prediction.wav"
model2 = load_model("model/WWD.h5")
is_linux=system() == 'Linux'
is_android = system() == 'Android'
song_queue = Queue()
r = sr.Recognizer()
CHUNK = 1024
FORMAT = paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 4500  # Soglia per il rilevamento audio
p = PyAudio()
stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
)
words, labels, model, data = load()
def stop_drivers():
    # Inserisci qui la logica per fermare i driver in modo pulito
    driver.quit()
    driverm.quit()
def text2Audio(text):
    # Inizializzare il motore di sintesi vocale
    engine = init()

    # Impostare le proprietà del motore di sintesi vocale
    engine.setProperty('rate', 150)  # velocità di riproduzione (parole per minuto)
    engine.setProperty('volume', 1)  # volume (0 to 1)
    # Pronunciare il testo
    engine.say(text)
    engine.runAndWait()

def response():
 with sr.Microphone() as source:
   text2Audio("Sii")
   audio = r.listen(source)
   try:
    text = r.recognize_google(audio, language="it-IT", show_all=False)
    text = text.lower()  # Converti il testo in minuscolo per semplificare la comparazione
    print(text)
                                
    if text=="stoppa" or text=="ferma" or text=="fermo":
        quit(driverm)
    elif text=="salta" or text=="skip" or text=="skippa":
        skippa(driverm)
    elif "musica" in text or "canzone" in text:
        text=canzone(text,"canzone")
        print(text)
        youtube_music_thread = threading.Thread(target=youtube_music, args=(text,driverm))
        youtube_music_thread.start()
    else:
     response = generate_response(text, words, labels, model, data)
     if response is None:
        response = pizzagpt(driver, text)
        print(response)
        text2Audio(response)
        #!!!!!!!IMPORTANTE!!!!!!
        #Se vuoi attivare la voce di Gerry usa questo comando
        #tts.talk(response)
     elif response=="bluetooth":
        text=text.split("connettiti a ")
        print(connect_to_device("MUSIC SOUND"))
     else:
        text2Audio(response)
   except:
     None


def ai2(model):
    myrecording = rec(int(seconds * fs), samplerate=fs, channels=2)
    wait()
    write(filename, fs, myrecording)

    audio, sample_rate = librosa.load(filename)
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfcc_processed = np.mean(mfcc.T, axis=0)

    prediction = model.predict(np.expand_dims(mfcc_processed, axis=0))
    print(prediction[:, 1])
    if prediction[:, 1] > 0.99:
       response()
def canzone(frase,parola_chiave):
    if parola_chiave=="canzone":
     parola_chiave = "canzone"
     indice_parola_chiave = frase.find(parola_chiave)
     if indice_parola_chiave != -1:
        nuova_frase = frase[indice_parola_chiave + len(parola_chiave):]
        return nuova_frase
     else:
        parola_chiave = "musica"
        indice_parola_chiave = frase.find(parola_chiave)
        if indice_parola_chiave != -1:
         nuova_frase = frase[indice_parola_chiave + len(parola_chiave):]
         return nuova_frase
        else:
         return frase
    elif parola_chiave=="playlist":
        indice_parola_chiave = frase.find(parola_chiave)
        if indice_parola_chiave != -1:
         nuova_frase = frase[indice_parola_chiave + len(parola_chiave):]
         return nuova_frase
        else:
         return frase
        

def start_listen():
  while True:
    audio_data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    if np.abs(audio_data).mean() > THRESHOLD:
        ai2(model2)
    else:
       continue

if __name__ == "__main__":
    start_listen()
    atexit.register(stop_drivers)
