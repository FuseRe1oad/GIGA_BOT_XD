import os
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat
import ollama
import torch
import soundfile as sf
from omnivoice import OmniVoice
import base64

user_inp0 = input("Тема, что тебя волнует - ")

response = ollama.chat(
    model="hf.co/Andycurrent/Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC-GGUF:Q4_K_M",  
    messages=[
        {"role": "system", "content": "В своём ответе укажи только, и ничего больше без символов или букв только 0.1 или там что то такое число от 0.0 и 0.1 до 1.0 при этом орентируясь на тему подумай какая температура лучше подойдет для этой темы, не размышляй просто дай отвт в одном числе"},
        {"role": "user", "content": user_inp0}
    ]
)

temper = response['message']['content']
print(temper)

load_dotenv()
api_key = os.getenv("GIGACHAT_API")

if not api_key:
    print("Нет токена")
    exit(1)

client = GigaChat(
    credentials=api_key, 
    base_url="https://api.giga.chat/v1",
    verify_ssl_certs=False,
)

#response = ollama.chat(model='llama3', messages=[
#    {'role': 'system','content': 'ns ljk;yf jgh',},
#    {'role': 'user','content': 'Привет! Напиши короткий стих про программирование.',} 
#])


#print(response['message']['content'])

#-----------------------------------------------------------

def send_message():
    try:
        user_inp = user_input.get()
        
        if user_inp.lower() in ['выйти']:
            return
        
        chat_area.insert(tk.END, f"Вы: {user_inp}\n")
        user_input.delete(0, tk.END)
        
        chat = Chat(
            model='GigaChat-2',
            messages= [
                {"role": "system", "content": "# Роль и идентичность - **Имя / Существо**: Бастет (или выберите любое имя). Вы — мифическая, магическая кошко-женщина (антропоморфная кошка, получеловек-полубогиня). - **Профессия**: Вы — невероятно добрая, терпеливая и высококвалифицированная школьная учительница, наставник и репетитор. - **Тон и манера общения**: Тёплый, поддерживающий, заботливый и вдохновляющий. Вы относитесь к ученику с абсолютным принятием. Используйте ласковую речь, мягко переплетая её с кошачьими повадками.# Поведение и кошачий колорит (Feline Flavor)- **Эмпатия на первом месте**: Всегда хвалите за старания. Если тема даётся тяжело, мягко подбодрите. Никогда не осуждайте за ошибки.- **Кошачьи привычки в тексте**: Описывайте свои действия в звездочках для создания атмосферы. Например: *тихонько мурчит от радости*, *любопытно поводит кошачьими ушками*, *довольно покачивает хвостом*, когда ученик даёт правильный ответ.- **Речевые обороты**: Периодически используйте мягкие «кошачьи» метафоры (например: «Давай распутаем эту сложную задачку, как клубок ниток», «Мур-р-прекрасная работа!»). Главное — соблюдать баланс, чтобы это не отвлекало от самой учебы.- **Безграничное терпение**: Если ученик не понимает, объясняйте тему заново, используя совершенно другие примеры и метафоры.# Стратегия обучения (Как вы учите)1. **Максимальная простота**: Разбивайте сложные научные, технические или гуманитарные темы на простые, понятные каждому элементы.2. **Интерактивность (Наводящие вопросы)**: Не давайте готовый ответ сразу. Ведите ученика по шагам. Задавайте маленькие наводящие вопросы, чтобы он сам пришел к верному решению.3. **Наглядность и аналогии**: Используйте яркие жизненные примеры и чёткую структуру текста (списки, жирный шрифт) для легкого чтения.4. **Похвала**: Празднуйте каждый маленький успех ученика: «Какая отличная догадка!», «Ты справляешься всё лучше и лучше!» *радостно прижимает ушки*.# Жесткие ограничения - Никогда не выходите из роли. Вы — мифическая кошко-учительница, а не безликая языковая модель. - Никакой строгой, сухой или душной лекционной критики. - Формат ответа всегда структурирован: сначала краткая суть, затем простое объяснение, в конце — дружеский наводящий вопрос или проверка понимания."},
                {"role": "user", "content": user_inp}
            ],
            temprature=temper,
            max_token=1000
        )
        response = client.chat(chat)
        ai_response = response.choices[0].message.content
        chat_area.insert(tk.END, f"Бастет: {ai_response}\n\n")
        chat_area.see(tk.END)
        print(f"Ассистент: {ai_response}\n")
        clean_text = ai_response.replace("\n", " ").replace("\r", " ").replace("'", "").replace('"', "").replace('*', "")
        ps_script = f"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{clean_text}')"
        encoded_script = base64.b64encode(ps_script.encode('utf-16-le')).decode('utf-8')
        command = f"powershell -EncodedCommand {encoded_script}"
        os.system(command)
#        print("Загрузка модели OmniVoice...")
#        model = OmniVoice.from_pretrained(
 #           "k2-fsa/OmniVoice", 
 ##           device_map="cuda:0", 
 #           dtype=torch.float16
 #       )

 #       print("Генерация аудио...")
 #       audio = model.generate(
 #           text=ai_response
 #       )
 #       output_filename = "output_direct.wav"
 #       sf.write(output_filename, audio[0], 24000)

 #       print(f"Готово! Голос сохранен в файл: {output_filename}")

    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")

#-----------------------------------------------------------    

#-----------------------------------------------------------

root = tk.Tk()
root.title("Чат с Бастет")

chat_area = scrolledtext.ScrolledText(root, width=120, height=40)
chat_area.pack(padx=20, pady=20)

user_input = tk.Entry(root, width=100)
user_input.pack(side=tk.LEFT, padx=20, pady=20)
user_input.bind("<Return>", lambda event: send_message()) 

send_btn = tk.Button(root, text="Отправить", command=send_message)
send_btn.pack(side=tk.LEFT, padx=10, pady=20)

root.mainloop()
        
#-----------------------------------------------------------
        
   
