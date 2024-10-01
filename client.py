#!/usr/bin/python3.11

from pvrecorder import PvRecorder
import pvporcupine
import data.config
import socket
import numpy as np
import struct
import sounddevice as sd
import json
import time
from vosk import Model, KaldiRecognizer


sock = None
recorder = None
porcupine = None
rec = None

def initialization():
    global sock
    global recorder
    global porcupine
    global rec
    #Init pvporcupine КЛИЕНТ
    porcupine = pvporcupine.create(
        access_key=data.config.PORCUPINE_api_key,
        keyword_paths=['./data/anthony_en_windows_v3_0_0.ppn'],
        sensitivities=[1])

    #INIT VOSK
    model = Model(lang="ru")
    rec = KaldiRecognizer(model, 16000)

    recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.0.101', 1354))

    recorder.start()

initialization()

def getting_voice():
    global sock
    voice_data=bytearray()
    while True:
        voice_bytes = sock.recv(4096)
        if voice_bytes.endswith(b'END'):
            voice_data.extend(voice_bytes[:-3])
            break
        voice_data.extend(voice_bytes)
    return np.frombuffer(voice_data, dtype=np.float32)

    
t=0
while True:
    pcm = recorder.read()
    keyword_index = porcupine.process(pcm)
    if keyword_index>=0:
        recorder.stop()
        sock.send("Энтони".encode('utf-8'))
        voice = getting_voice()
        sd.play(voice,24000)
        sd.wait() 
        recorder.start()
        t=time.time()
    while time.time()-t<=5:
        pcm = recorder.read()
        data = struct.pack("h" * len(pcm), *pcm)
        if rec.AcceptWaveform(data):
            recorder.stop()
            result = rec.Result()
            text=json.loads(result)["text"]
            if len(text)>0:
                sock.send(text.encode('utf-8'))
                voice = getting_voice()
                sd.play(voice,24000)
                sd.wait()
            t=time.time()
            recorder.start()
    