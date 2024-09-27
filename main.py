#!/home/genichi/myenv/bin/python


from vosk import Model, KaldiRecognizer
import json
from groq import Groq
import pyaudio
import time
from os import system
def START():
    RATE = 16000  # Частота дискретизации
    FORMAT = pyaudio.paInt16  # Формат данных (16 бит)
    CHANNELS = 1  # Количество каналов (моно)
    CHUNK = 1024  # Размер блока данных

    #vosk
    model = Model(lang="ru")
    rec = KaldiRecognizer(model, RATE)

    
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    stream.start_stream()


    mes=[
        {
            "role":"user",
            "content": "Запомни, тебя зовут Эдди, полное имя Эддисон"
        },
        {
            "role":"assistant",
            "content": "Запомнил, хозяин"
        }
    ]

    client = Groq(api_key="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")
    # Запись и обработка
    t=0
    while True:
        text=""
        data = stream.read(CHUNK)  # Чтение данных из микрофона
        if rec.AcceptWaveform(data):  # Если распознано слово, выводим результат
            result = rec.Result()
            text=json.loads(result)["text"]
            if "эдди" in text or "эддисон" in text or time.time()-t<=10:
                t=time.time()
                print(text)
            
                if "что у меня за система" in text:
                    system('neofetch')

                elif "выключи ноутбук" in text:
                    system('poweroff')

                elif "стоп" in text:
                    break
                elif len(text)>2:
                    mes.append({"role":"user", "content":f"{text}"})
                    chat_completion = client.chat.completions.create(messages=mes,model="llama-3.2-90b-text-preview", temperature = 1, max_tokens=1024, top_p=1, stop=None)
                    response = chat_completion.choices[0].message.content
                    mes.append({"role":"assistant", "content":response})
                    print(response)
    # Остановка и закрытие потоков
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print(mes)

START()
