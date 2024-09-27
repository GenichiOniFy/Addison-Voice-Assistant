#!/bin/python

from os import system

system("cd /home/genichi/Yandex.Disk/Addison-Voice-Assistant/")

while True:
    system(f'echo "{input()}" > /home/genichi/Yandex.Disk/Addison-Voice-Assistant/input.file')
