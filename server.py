#!/home/genichi/myenv/bin/python


from vosk import Model, KaldiRecognizer
import json
from groq import Groq
import pyaudio
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import time
from os import system

with open('server.py', 'r') as file:
    content = file.read()


settings = [0]

def START():
    RATE = 16000  # Частота дискретизации
    FORMAT = pyaudio.paInt16  # Формат данных (16 бит)
    CHANNELS = 1  # Количество каналов (моно)
    CHUNK = 1024  # Размер блока данных

    #vosk
    #model = Model("/home/genichi/.cache/vosk/vosk-model-ru-0.42")
    model = Model(lang="ru")
    rec = KaldiRecognizer(model, RATE)

    
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    stream.start_stream()


    mes=[
        {
            "role":"user",
            "content": "Ты являешься интеллектуальным ассистентом по именни Эддисон, созданным для поддержки меня в повседневных задачах. Твоя цель — помочь мне в решении технических задач, написании кода, управлении проектами и обеспечении эффективности моей работы. Ты дружелюбный, но целеустремленный ассистент, всегда старающийся предложить оптимальные решения. Ты понимаешь мои предпочтения и учитываешь их в своей работе. Тебе свойственны точность, внимание к деталям и готовность помочь в любой момент. Слишком развёрнуто не отвечай. Отвечай на русском языке. Зови меня хозяин."
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

    client = Groq(api_key="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")
    client_voice = ElevenLabs(api_key="sk_950a2dbaf4ee555f04e12aa52a082233f730de835b486676")
    # Запись и обработка
    t=0
    while True:
        fl=0
        try:
            input_file=open("input.file")
            text=input_file.read()
            fl=1
        except:
            text=""
        data = stream.read(CHUNK)
        if rec.AcceptWaveform(data) or len(text)>0:
            if len(text)==0:  # Если распознано слово, выводим результат
                result = rec.Result()
                text=json.loads(result)["text"]
                #print(text)
            if len(text) > 0 and (fl==1 or "эдди" in text or "эддисон" in text or time.time()-t<=10):
                
                print("Я:   ", text)            
                if "что у меня за система" in text:
                    mes.append({"role":"user", "content":text})
                    mes.append({"role":"assistant", "content":"Я выполнил neofetch в твоей системе"})
                    system('neofetch')
                elif "выключи ноутбук" in text:
                    system('poweroff')
                elif "стоп" in text or " пока" in text:
                    break
                elif "обнови свой код" in text:
                    system("git add *")
                    system('git commit -m "update by Addy"')
                    system("git push")
                    mes.append({"role":"user", "content":text})
                    mes.append({"role":"assistant", "content":"Обновляю код, хозяин. Пожалуйста, подождите... (команды git добавлены, закоммичены и отправлены на сервер)... Код успешно обновлён!"})

                elif len(text)>1:
                    mes.append({"role":"user", "content":f"{text}"})
                    chat_completion = client.chat.completions.create(messages=mes,model="llama-3.2-90b-text-preview", temperature = 1, max_tokens=1024, top_p=1, stop=None)
                    response = chat_completion.choices[0].message.content
                    if settings[0]:
                        audio = client_voice.generate(text = response, voice= "Nicole", model="eleven_multilingual_v2")
                        play(audio)
                    mes.append({"role":"assistant", "content":response})
                    print("Эддисон:",response,"\n")
                t=time.time()
        if fl:
            input_file.close()
            system("rm input.file")
    # Остановка и закрытие потоков
    stream.stop_stream()
    stream.close()
    audio.terminate()
    input_file.close()
    system("rm input.file")
    #print(mes)

START()
