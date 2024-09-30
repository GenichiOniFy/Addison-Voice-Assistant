#!/sbin/python3.11
from vosk import Model, KaldiRecognizer
import json
from groq import Groq
import socket
import data.config as config
import struct
from data.class_voice_assistant import voice_assistant
import time
import re
import sounddevice as sd
from os import system


antony = None
conn = None
pattern = r'system\((.*?)\)'

def initialization():
    #INIT VOSK
    model = Model(lang="ru")
    rec = KaldiRecognizer(model, 16000)

    #INIT GROQ
    llm = Groq(api_key=config.GROQ_api_key)

    #CREAT ANTONY
    global antony
    important_memory = json.load(open('data/memory.json', 'r', encoding='utf-8'))
    important_memory.append({"role":"user","content":f'Вот твой исходный код: {open("server.py", "r", encoding="utf-8").read()}'})
    antony = voice_assistant(llm, "antony", "ru",important_memory=important_memory)


    #INIT SERVER-SOCKET
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 1348))
    sock.listen()

    with sock:
        print("Сервер ожидает соединения...")
        global conn
        conn, addr = sock.accept()
        print(f"Подключен клиент: {addr}")


initialization()

def bot_system(res):
    matches = re.findall(pattern, res)
    for match in matches:
        system(f'{match}')


while True:
    response = antony.think(conn.recv(4096).decode('utf-8'))
    conn.send(response.encode('utf-8'))
    bot_system(response)
    

