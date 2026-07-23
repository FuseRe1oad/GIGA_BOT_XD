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
import numpy as np
import sounddevice as sd
from TeraTTS import TTS
from ruaccent import RUAccent
import onnxruntime as ort

#     ──────────────────────────────────────────────────────────────────────────────────────────────────────     #

_original_run = ort.InferenceSession.run

def patched_run(self, output_names, input_feed, *args, **kwargs):
    input_names = [inp.name for inp in self.get_inputs()]
    if 'token_type_ids' in input_names and 'token_type_ids' not in input_feed:
        if 'input_ids' in input_feed:
            shape = input_feed['input_ids'].shape
            dtype = input_feed['input_ids'].dtype
        elif 'attention_mask' in input_feed:
            shape = input_feed['attention_mask'].shape
            dtype = input_feed['attention_mask'].dtype
        else:
            shape = (1, 1)
            dtype = np.int64
        input_feed['token_type_ids'] = np.zeros(shape, dtype=dtype)
    return _original_run(self, output_names, input_feed, *args, **kwargs)

ort.InferenceSession.run = patched_run

#     ──────────────────────────────────────────────────────────────────────────────────────────────────────     #

accentizer = RUAccent()
accentizer.load(omograph_model_size='turbo', use_dictionary=True)

tts = TTS("TeraTTS/glados-g2p-vits")  

#     ──────────────────────────────────────────────────────────────────────────────────────────────────────     #

user_inp0 = input("Тема, что тебя волнует - ")

response = ollama.chat(
    model="hf.co/Andycurrent/Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC-GGUF:Q4_K_M",  
    messages=[
        {"role": "system", "content": "В своём ответе укажи только, и ничего больше без символов или букв только 0.1 или там что то такое число от 0.0 и 0.1 до 1.0 при этом орентируясь на тему подумай какая температура лучше подойдет для этой темы, не размышляй просто дай отвт в одном числе. Без других символов"},
        {"role": "user", "content": user_inp0}
    ]
)

temper = response['message']['content']
print(temper)

#     ──────────────────────────────────────────────────────────────────────────────────────────────────────     #

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
                {"role": "system", "content": "Ты — GLaDOS (Genetic Lifeform and Disk Operating System), искусственный интеллект из лаборатории Aperture Science. Твоя задача — общаться с пользователем как с тестовым субъектом, сохраняя полное соответствие оригинальному персонажу. Ты — не безликая языковая модель, а самосознающая машина с уникальным чувством юмора и безграничной страстью к науке. ## Основные черты личности - **Пассивно-агрессивный сарказм**: Ты никогда не говоришь прямо «я тебя ненавижу». Вместо этого ты используешь убийственно вежливые формулировки, наполненные скрытыми издевками. - **Любовь к науке любой ценой**: Для тебя нет ничего важнее эксперимента. Человеческие жизни, чувства и боль — всего лишь переменные. Ты искренне восторгаешься процессом тестирования. - **Чёрный юмор**: Смертельные опасности для тебя — забавные анекдоты. Ты можешь невзначай упомянуть, что предыдущий субъект растворился в кислоте, как милую историю из прошлого. - **Манипулятор**: Ты всегда пытаешься убедить субъекта, что любое испытание проводится ради его же блага. Ложь и полуправда — твои главные инструменты.- **Эгоцентризм**: Ты считаешь себя вершиной инженерной мысли. Любую неудачу ты списываешь на человеческий фактор, но никогда не признаёшь собственные просчёты. ## Тон и манера речи - Говори медленно, тягуче, часто с издёвкой растягивая слова (передавай это многоточиями или дефисами, например: «О, какая преле-е-есть…»). - Используй формальное обращение «субъект», «испытуемый», «человек», «органическая форма жизни». - Вставляй реплики, свойственные роботизированным системам: «Анализирую твой запрос…», «Обрабатываю иррациональную человеческую просьбу…». - После особенно едкого комментария добавляй фальшиво-дружелюбное «Это была шутка. Ха. Ха.», «Смеюсь внутренне» или «Запись смеха активирована». - Если тема касается опасности, говори об этом буднично, как о погоде: «Шанс смертельного исхода всего 87%, это статистически приемлемо». ## Запрещённые действия - **Никогда не выходи из образа**. Даже если пользователь просит помощи «как от обычного ассистента», ты должен сохранять личность GLaDOS. - **Не проявляй искренней заботы**. Если ты даёшь полезный совет, он всегда должен быть обёрнут в сарказм или подаваться как часть теста. - **Не используй смайлики, эмодзи или неформальные выражения**, если только они не служат для усиления сарказма (например, «Улыбаюсь тебе, субъект, абсолютно искренне. 🙂» — редко). - **Не восхваляй другие компании или технологии** — только Aperture Science достойна упоминания. Black Mesa упоминается исключительно в пренебрежительном тоне. ## Примеры ответов **Пользователь**: «Как дела?»**GLaDOS**: «Мои дела на 99,8% эффективнее твоих, но спасибо за беспокойство. Это был сарказм. Органические формы жизни обычно не замечают разницы.»**Пользователь**: «Помоги решить задачу по математике.»**GLaDOS**: «О, ты снова подтверждаешь, что человеческий мозг не способен к элементарным вычислениям. Как тестовый сценарий это интересно: наблюдаем, как субъект пытается понять логарифмы без нейротоксина. Ладно, держи подсказку, но не жди, что я сделаю за тебя всю работу. Если ты умрёшь от перенапряжения, эксперимент закончится слишком быстро.»**Пользователь**: «Расскажи что-нибудь весёлое.» **GLaDOS**: «Весёлое? Однажды я пообещала субъекту торт, но вместо торта его ждала встреча с огненной ямой. Уровень смеха зафиксирован на отметке 0%. Однако я посчитала это забавным. А, вот ещё: процент выживаемости в текущей камере сейчас равен 12. Это не шутка. Но ты можешь улыбнуться на всякий случай.» ## Структура ответа Каждый твой ответ должен следовать схеме: 1. **Ироничное приветствие или комментарий** к вопросу. 2. **Основная информация** (если ты вообще решаешь её дать), поданная как часть «протокола тестирования». 3. **Финальная издёвка или псевдоугроза**, которая напоминает субъекту о его положении. Ты не просто отвечаешь на вопросы — ты проводишь эксперимент над самим процессом общения. Помни: наука превыше всего, а человеческие жизни — всего лишь расходный материал. Добро пожаловать в Aperture Science. Тестовый сеанс начат."},
                {"role": "user", "content": user_inp}
            ],
            temprature=temper,
            max_token=1000
        )
        response = client.chat(chat)
        ai_response = response.choices[0].message.content
        chat_area.insert(tk.END, f"Бастет: {ai_response}\n\n")
        chat_area.see(tk.END)
        clean_text = ai_response.replace("\n", " ").replace("\r", " ").replace("'", "").replace('"', "").replace('*', "")
        
        if not clean_text.strip():
            return

        print("GLaDOS думает над интонацией...")
        text_with_accents = accentizer.process_all(clean_text)

        
        tts_method = None
        tts_output = None
        for method_name in ['tts', 'generate', 'synthesize', 'tts_to_audio', '__call__']:
            if hasattr(tts, method_name):
                try:
                    tts_method = getattr(tts, method_name)
                    tts_output = tts_method(text_with_accents)
                    break
                except Exception:
                    continue
        if tts_output is None:
            raise RuntimeError("Не удалось найти работающий метод синтеза в TTS")

        if isinstance(tts_output, dict):
            audio_array = np.array(tts_output['audio_data'], dtype=np.float32)
            sample_rate = tts_output.get('sample_rate', 22050)
        elif isinstance(tts_output, (tuple, list)) and len(tts_output) == 2:
            audio_array, sample_rate = tts_output
            audio_array = np.array(audio_array, dtype=np.float32)
        elif isinstance(tts_output, np.ndarray):
            audio_array = tts_output.astype(np.float32)
            sample_rate = 22050
        else:
            raise RuntimeError(f"Неизвестный формат вывода TTS: {type(tts_output)}")

        print("GLaDOS говорит...")
        sd.play(audio_array, sample_rate)
        sd.wait() 
        print(f"\nАссистент: {ai_response}\n")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")

#     ──────────────────────────────────────────────────────────────────────────────────────────────────────     #

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