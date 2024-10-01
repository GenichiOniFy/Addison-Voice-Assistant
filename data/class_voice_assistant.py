from os import system

class voice_assistant:
    def __init__(self, llm, name="bot", language="en", temp_memory=[], important_memory=[], tts_set=None):
        self.name = name
        self.language = language
        self.temp_memory = temp_memory
        self.important_memory = important_memory
        self.llm = llm
        self.modelTTS = tts_set
        print("\nThe voice assistant has been successfully created")
    def think(self, request):
        if len(request)>0:
            print(f"Клиент: {request}")
            self.temp_memory.append({"role":"user", "content":f"{request}"})
            chat_completion = self.llm.chat.completions.create(messages=self.important_memory+self.temp_memory,model="llama-3.2-90b-text-preview", temperature = 1, max_tokens=1024, top_p=1, stop=None)
            response = chat_completion.choices[0].message.content
            print(f"Энтони: {response}")
            self.temp_memory.append({"role":"assistant", "content":response})
            return response+'\n'
    def speak(self, data):
        voice = self.modelTTS.apply_tts(text=data + "...",
                            speaker='eugene',
                            sample_rate=24000,
                            put_accent=True,
                            put_yo=True)
        
        voice_np = voice.numpy()
        voice_bytes = voice_np.tobytes()
        print(len(voice_bytes))

        return voice_bytes