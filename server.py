#!/sbin/python3.11
import json
from groq import Groq
import socket
import data.config as config
import struct
from data.class_voice_assistant import voice_assistant
import time
import subprocess
import data.server_telegram as tg_bot
import threading
import torch
import re
import sounddevice as sd
from os import system


anthony = None
conn = None
pattern = r'system\((.*?)\)'

def init_telegram_bot():
    tg_bot.init(config.TELEGRAM_token)

def initialization():

    #INIT GROQ
    llm = Groq(api_key=config.GROQ_api_key)

    #Init TTS
    modelTTS, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language='ru',
                          speaker='v4_ru')
    modelTTS.to(torch.device('cpu'))

    #CREAT ANTHONY
    global anthony
    important_memory = json.load(open('data/memory.json', 'r', encoding='utf-8'))
    important_memory.append({"role":"user","content":f'Вот твой исходный код: {open("server.py", "r", encoding="utf-8").read()}'})
    anthony = voice_assistant(llm, "anthony", "ru",important_memory=important_memory, tts_set=modelTTS)


    #INIT SERVER-SOCKET
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 1363))
    sock.listen()

    

    with sock:
        print("Сервер ожидает соединения...")
        global conn
        bot_thread=threading.Thread(target=init_telegram_bot)
        bot_thread.start()
        
        conn, addr = sock.accept()
        print(f"Подключен клиент: {addr}")
    
    
    


initialization()

def bot_system(res):
    matches = re.findall(pattern, res)
    for match in matches:
        command = f"{match}"[1:-1]
        result_command=subprocess.check_output(command,shell=True)
        conn.send(result_command+b'COMMAND')
        anthony.temp_memory.append({"role":"assistant","content":f"Выполнил команду: {result_command.decode('utf-8')}"})
        


while True:
    response = anthony.think(conn.recv(4096).decode('utf-8')).encode('utf-8')
    bot_system(response.decode('utf-8'))
    
    if 0:
        response = anthony.speak(response.decode('utf-8'))+b'VOICE'
    else:
        response+=b''
    conn.send(response)

