#!/usr/bin/python3.11
from vosk import Model, KaldiRecognizer
import json
from groq import Groq
import struct
import pvporcupine
from class_voice_assistant import voice_assistant
import time
import re
import sounddevice as sd
import torch
from pvrecorder import PvRecorder
from os import system


antony = None

def initialization():
    #Init vosk
    model = Model(lang="ru")
    rec = KaldiRecognizer(model, 16000)

    #Init pvporcupine
    porcupine = pvporcupine.create(
        access_key="agqOkA4/tqSDr25RFY0f4zDh/IiLR55y1cVu929QYKlTwyCKmg0dgg==",
        keyword_paths=['/home/genichi/Yandex.Disk/Antony-Voice-Assistant/antony_en_linux_v3_0_0.ppn'],
        sensitivities=[1])

    #Init TTS
    modelTTS, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language='ru',
                          speaker='v4_ru')
    modelTTS.to(torch.device('cpu'))
    
    llm = Groq(api_key="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")

    global antony
    antony = voice_assistant(llm, "antony", "ru")


initialization()


while True:
    print(antony.think(input()))
