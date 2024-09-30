from os import system

class voice_assistant:
    def __init__(self, llm, name="bot", language="en", temp_memory=[], important_memory=[]):
        self.name = name
        self.language = language
        self.temp_memory = temp_memory
        self.important_memory = important_memory
        self.llm = llm
        print("\nThe voice assistant has been successfully created")
    def think(self, request):
        if "что у меня за система" in request:
            self.temp_memory.append({"role":"user", "content":request})
            self.temp_memory.append({"role":"assistant", "content":"Я выполнил neofetch в твоей системе"})
            return 'system("neofetch")\n'
        elif "выключи ноутбук" in request:
            return 'system("poweroff")\n'
        elif "обнови свой код" in request:
            system("git add *")
            system('git commit -m "update by Tony"')
            system("git push")
            response = "Обновляю код, хозяин. Пожалуйста, подождите... (команды git добавлены, закоммичены и отправлены на сервер)... Код успешно обновлён!\n"
            self.temp_memory.append({"role":"user", "content":request})
            self.temp_memory.append({"role":"assistant", "content":response})
            return response
        elif len(request)>0:
            self.temp_memory.append({"role":"user", "content":f"{request}"})
            chat_completion = self.llm.chat.completions.create(messages=self.important_memory+self.temp_memory,model="llama-3.2-90b-text-preview", temperature = 1, max_tokens=1024, top_p=1, stop=None)
            response = chat_completion.choices[0].message.content
            self.temp_memory.append({"role":"assistant", "content":response})
            return response+'\n'