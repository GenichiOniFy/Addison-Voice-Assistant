#!/usr/bin/python3.11

from vosk import Model, KaldiRecognizer
import json
from groq import Groq
import struct
import pvporcupine
import time
import re
import spacy
import sounddevice as sd
import torch
from pvrecorder import PvRecorder
from os import system



with open('/home/genichi/Yandex.Disk/Antony-Voice-Assistant/server.py', 'r') as file:
    content = file.read()

settings = [1]


nlp = spacy.load("ru_core_news_sm")





porcupine = pvporcupine.create( #+
    access_key="agqOkA4/tqSDr25RFY0f4zDh/IiLR55y1cVu929QYKlTwyCKmg0dgg==", #+
    keyword_paths=['/home/genichi/Yandex.Disk/Antony-Voice-Assistant/antony_en_linux_v3_0_0.ppn'], #+
    sensitivities=[1] #+
) #+

#TTS_set
modelTTS, _ = torch.hub.load(repo_or_dir='snakers4/silero-models', #+
                          model='silero_tts', #+
                          language='ru', #+
                          speaker='v4_ru') #+
modelTTS.to(torch.device('cpu')) #+



def va_speak(what: str):
    ti=time.time()
    audio = modelTTS.apply_tts(text=what + "..",
                            speaker='eugene',
                            sample_rate=48000,
                            put_accent=True,
                            put_yo=True)


    print(time.time()-ti)
    sd.play(audio, 48000*1.03)
    time.sleep((len(audio) / 48000*1.03) + 0.5)
    sd.stop()


def START():
    #vosk
    #model = Model("/home/genichi/.cache/vosk/vosk-model-ru-0.42")
    model = Model(lang="ru") #+
    rec = KaldiRecognizer(model, 16000) #+


    recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
    recorder.start()


    mes=[
        {
            "role":"user",
            "content": "Ты являешься интеллектуальным ассистентом по именни Энтони,\
                  созданным для поддержки меня в повседневных задачах.\
                      Твоя цель — помочь мне в решении технических задач, написании кода,\
                          управлении проектами и обеспечении эффективности моей работы.\
                              Ты дружелюбный, но целеустремленный ассистент,\
                                  всегда старающийся предложить оптимальные решения.\
                                      Ты понимаешь мои предпочтения и учитываешь их в своей работе.\
                                          Тебе свойственны точность, внимание к деталям и готовность помочь в любой момент.\
                                              Слишком развёрнуто не отвечай.\
                                                  Отвечай на русском языке.\
                                                     Зови меня хозяин.\
                                                        Если я скажу тебе что-то выполнить в системе, то используй команду system('командав')"
        },
        {
            "role":"user",
            "content":f"Вот твой исходный код: {content}"
        },
        {
            "role":"assistant","role":"user",
            "content": "Запомнил, хозяин."
        }
        
        ]

    client = Groq(api_key="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") #+

    # Запись и обработка
    t=0
    
    while True:
        fl=0
        try:
            input_file=open("/home/genichi/Yandex.Disk/Antony-Voice-Assistant/input.file")
            text=input_file.read()
            fl=1
        except:
            text=""
        #data = stream.read(CHUNK)
        pcm = recorder.read()
        keyword_index = porcupine.process(pcm)
        if keyword_index>=0:
            recorder.stop()
            print("Да, хозяин.")
            if settings[0]:
                va_speak("Да, хозяин")
            recorder.start()
            t=time.time()
        while time.time()-t<=5 or len(text)>0:
            pcm = recorder.read()
            data = struct.pack("h" * len(pcm), *pcm)
            if rec.AcceptWaveform(data):
                recorder.stop()
                if len(text)==0:  # Если распознано слово, выводим результат
                    result = rec.Result()
                    text=json.loads(result)["text"]
                    print(text)
                if len(text) > 0 or fl==1:
                    print("Я:   ", text)            
                    if "что у меня за система" in text: #+
                        mes.append({"role":"user", "content":text}) #+ 
                        mes.append({"role":"assistant", "content":"Я выполнил neofetch в твоей системе"}) #+
                        system('neofetch') #+
                    elif "выключи ноутбук" in text: #+
                        system('poweroff') #+
                    elif "обнови свой код" in text: #+
                        system("git add *") #+
                        system('git commit -m "update by Addy"') #+
                        system("git push") #+
                        mes.append({"role":"user", "content":text}) #+
                        mes.append({"role":"assistant", "content":"Обновляю код, хозяин. Пожалуйста, подождите... (команды git добавлены, закоммичены и отправлены на сервер)... Код успешно обновлён!"}) #+

                    elif len(text)>1: #+
                        mes.append({"role":"user", "content":f"{text}"})#+
                        chat_completion = client.chat.completions.create(messages=mes,model="llama-3.2-90b-text-preview", temperature = 1, max_tokens=1024, top_p=1, stop=None) #+
                        response = chat_completion.choices[0].message.content #+
                        print("Энтони:",response,"\n")
                        if settings[0]:
                            va_speak(response)
                        pattern = r'system\((.*?)\)'
                        matches = re.findall(pattern, response)
                        for match in matches:
                            print(match)
                            system(f'{match}')
                        mes.append({"role":"assistant", "content":response}) #+
                    t=time.time()
                recorder.start()
                break
        if fl:
            input_file.close()
            system("rm /home/genichi/Yandex.Disk/Antony-Voice-Assistant/input.file")

START()
