#!/usr/bin/python


from vosk import Model, KaldiRecognizer
import json
import pyaudio
from os import system
def START():
    RATE = 16000  # Частота дискретизации
    FORMAT = pyaudio.paInt16  # Формат данных (16 бит)
    CHANNELS = 1  # Количество каналов (моно)
    CHUNK = 1024  # Размер блока данных

    #vosk
    model = Model("~/.cache/vosk/vosk-model-ru-0.42")
    rec = KaldiRecognizer(model, RATE)

    
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    stream.start_stream()

    # Запись и обработка
    while True:
        data = stream.read(CHUNK)  # Чтение данных из микрофона
        if rec.AcceptWaveform(data):  # Если распознано слово, выводим результат
            result = rec.Result()
            text=json.loads(result)["text"]
            print(text)
            
            if text == "эдди что у меня за система":
                system('neofetch')

            if text == "эдди выключи ноутбук":
                system('poweroff')

            if text == "эдди стоп":
                break

    # Остановка и закрытие потоков
    stream.stop_stream()
    stream.close()
    audio.terminate()

START()
