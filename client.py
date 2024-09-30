#!/usr/bin/python3.11

from pvrecorder import PvRecorder
import pvporcupine
import data.config
import torch
import socket

def initialization():
    #Init pvporcupine КЛИЕНТ
    porcupine = pvporcupine.create(
        access_key=data.config.PORCUPINE_api_key,
        keyword_paths=['/home/genichi/Yandex.Disk/Anthony-Voice-Assistant/data/anthony_en_linux_v3_0_0.ppn'],
        sensitivities=[1])

    #Init TTS КЛИЕНТ
    modelTTS, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language='ru',
                          speaker='v4_ru')
    modelTTS.to(torch.device('cpu'))


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('0.0.0.0', 1348))

initialization()