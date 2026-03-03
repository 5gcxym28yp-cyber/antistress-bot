import telebot
from telebot import types
import time
import random
import os
from flask import Flask, request
import threading

print("=" * 60)
print("🧘 ЗАПУСК АНТИСТРЕСС БОТА (WEBHOOK)")
print("=" * 60)

# ===== ТОКЕН БОТА =====
# ВАЖНО: Замени на свой токен от BotFather!
TOKEN = os.environ.get('BOT_TOKEN', '8646403851:AAE8UsPKh-NSdvniNt84bX32BTuVomWYNQ0')
bot = telebot.TeleBot(TOKEN)

# ===== FLASK ДЛЯ WEBHOOK =====
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🧘 Антистресс Гид</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #6B5B95, #9B59B6); color: white; }
            .container { background: rgba(255,255,255,0.1); padding: 40px; border-radius: 30px; max-width: 600px; margin: 0 auto; }
            .status { background: #2ecc71; padding: 15px 30px; border-radius: 50px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧘 Антистресс Гид</h1>
            <div class="status">✅ Работает 24/7</div>
            <p>Бот для помощи детям в стрессовых ситуациях</p>
            <p>Нажми /start в Telegram</p>
        </div>
    </body>
    </html>
    """

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/health')
def health():
    return {"status": "active"}, 200

@app.route('/ping')
def ping():
    return "pong", 200

# ===== ДАННЫЕ ПОЛЬЗОВАТЕЛЕЙ =====
user_states = {}

# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "😨 Боюсь отвечать у доски",
        "📚 Трясет перед контрольной",
        "👥 С ребятами сложно",
        "😡 Поссорился с другом",
        "😴 Устал и ничего не хочу",
        "🎮 Поиграем?",
        "🔥 Помоги прямо сейчас!"
    ]
    for i in range(0, len(buttons), 2):
        if i+1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])
    return markup

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = f"""🧘 *Привет, {message.from_user.first_name}!*

Я – *«Антистресс Гид»* – твой личный помощник, который всегда рядом.

Меня создал ученик 3 класса Эльдар вместе со школьным психологом. Мы провели исследование в 3-4 классах и узнали, что вас волнует больше всего.

Я не кусаюсь, не ставлю оценки и не ругаю. Я просто помогу тебе успокоиться, если страшно, обидно или грустно.

*Выбирай, что случилось 👇*"""
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=main_menu())

# ===== 1. БОЮСЬ ОТВЕЧАТЬ У ДОСКИ =====
@bot.message_handler(func=lambda m: m.text == "😨 Боюсь отвечать у доски")
def fear_blackboard(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🟢 Готовлюсь дома", callback_data="fear_home"),
        types.InlineKeyboardButton("🟡 Сейчас выйду к доске", callback_data="fear_now"),
        types.InlineKeyboardButton("🔴 Уже стою у доски", callback_data="fear_at_board")
    )
    text = """😨 *Боюсь отвечать у доски*

О, это знакомо! Сердце – в пятки, коленки дрожат, голос пропадает? Это организм включает режим «Внимание, опасность!», хотя на самом деле опасности нет.

*Выбери свою ситуацию:*"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "fear_home")
def fear_home(call):
    text = """🟢 *Готовлюсь дома*

Круто, что готовишься заранее! Это уже полпобеды 💪

Чтобы дома было не страшно, попробуй упражнение *«Театр одного актера»*:

1️⃣ Посади свои игрушки в ряд – это будет твой класс. Расскажи им стихотворение или правило громко, с выражением. Игрушки – зрители благодарные, не перебивают 😊

2️⃣ Потом расскажи это же, стоя перед стулом – представляя, что на стуле сидит учитель.

3️⃣ А теперь – перед зеркалом, глядя себе в глаза.

Всего 3-4 раза – и мозг привыкнет, что текст звучит вслух. Завтра у доски будет уже не страшно, а привычно. Проверено! 🔥"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=back_to_main())

@bot.callback_query_handler(func=lambda call: call.data == "fear_now")
def fear_now(call):
    text = """🟡 *Сейчас выйду к доске*

Ой, это самое волнительное – когда уже вот-вот, а еще не начал. Сердце выпрыгивает, ладошки мокрые, в голове туман. Сейчас поможем! 🌪️

Пока учитель вызывает кого-то другого или пишет на доске, сделай НЕЗАМЕТНО для других три действия:

1️⃣ Сильно-сильно прижми ступни к полу. Почувствуй, как ты стоишь на земле. Ты крепкий, как дерево 🌳

2️⃣ Сделай *«Квадратное дыхание»* про себя:
Вдох (1,2,3,4) – задержка (1,2,3,4) – выдох (1,2,3,4) – задержка (1,2,3,4). Только один раз, пока никто не видит.

3️⃣ Прошепчи губами (без звука): *«Я знаю. Я смогу. Я справлюсь»*. Это как заклинание от страха ✨

Когда выйдешь – первые 3 секунды смотри не на класс, а на доску или в окно. Соберись с мыслями. А потом поворачивайся и говори.

*Ты готов!* 💪"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=back_to_main())

@bot.callback_query_handler(func=lambda call: call.data == "fear_at_board")
def fear_at_board(call):
    text = """🔴 *Уже стою у доски*

Окей, ты у доски, все смотрят. Самое страшное уже позади – ты вышел. Теперь главное – не торопиться 🧘

▶️ *Правило 3 секунд*. Ничего не говори первые 3 секунды. Просто посмотри в окно, на доску или на потолок. Сделай вид, что собираешься с мыслями. Это перезагрузит мозг и успокоит дыхание.

🗣️ Если чувствуешь, что голос дрожит – сделай вид, что прочищаешь горло (негромко кашляни). Это расслабит связки.

💡 Если вдруг забыл, что говорить – не молчи в ужасе. Скажи честно: *«Можно я начну с примера?»* или *«Я сейчас вспомню, секунду»*. Учителя это разрешают. А пока говоришь – память включится!

👥 И главное: класс – это просто люди. Они такие же, как ты. Многие вообще не слушают, а думают о своём. Так что выдыхай и рассказывай спокойно!

*Ты справишься!* 💪"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=back_to_main())

# ===== 2. ТРЯСЕТ ПЕРЕД КОНТРОЛЬНОЙ =====
@bot.message_handler(func=lambda m: m.text == "📚 Трясет перед контрольной")
def fear_test(message):
    text = """📚 *Трясет перед контрольной*

Контрольная – это марафон, а не спринт. Тут главное – правильно распределить силы. Я дам тебе алгоритм *«Чип и Дейв спешат на помощь»*. Запомни три буквы: Ч, И, П 📚

🔵 *Ч* – Чтение. Когда получишь лист с заданиями, не хватайся за ручку. Сначала просто прочитай ВСЕ задания глазами. Как разведчик изучает карту. Ничего не решай, просто смотри.

🟢 *И* – Ищем легкое. Найди задание, которое тебе кажется самым простым. То, что ты точно умеешь делать. Начни с него. Это как разминка перед спортом – разогреешь мозг.

🟡 *П* – Пропускай. Если задание сложное и тормозит тебя – ПРОПУСТИ его! Отметь номер в черновике и иди дальше. Решай то, что знаешь. А к сложным вернешься потом, с новыми силами.

🧊 *И главный секрет:* если прямо сейчас трясет – сделай Квадратное дыхание:
Вдох (1,2,3,4) – задержка (1,2,3,4) – выдох (1,2,3,4) – задержка (1,2,3,4).
Повтори 3 раза. Готово! Ты спокоен и собран. Покажи им, на что способен! 💪🔥"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=back_to_main())

# ===== 3. С РЕБЯТАМИ СЛОЖНО =====
@bot.message_handler(func=lambda m: m.text == "👥 С ребятами сложно")
def social(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🚫 Никто не хочет играть", callback_data="social_play"),
        types.InlineKeyboardButton("😰 Страшно подойти к компании", callback_data="social_approach"),
        types.InlineKeyboardButton("🙊 Кажется, что смеются надо мной", callback_data="social_laugh")
    )
    text = """👥 *С ребятами сложно*

Бывает, что кажется, будто другие обсуждают тебя или не хотят с тобой общаться? Это называется социальный стресс. Давай разбираться. Что именно случилось?"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "social_play")
def social_play(call):
    text = """🚫 *Никто не хочет играть*

Это обидно, согласен. Сразу кажется, что ты какой-то не такой. Но часто бывает, что дети просто увлечены своей игрой и не замечают никого вокруг. Это не про тебя лично.

Вот тебе *«Секретный план внедрения»* 🤫:

1️⃣ Найди в компании того, кто смотрит по-доброму, и просто улыбнись ему.

2️⃣ Не спрашивай *«Можно с вами?»* (на это часто говорят «нет»). Лучше подойди и спроси: *«Классная игра! А кем тут быть самым сложным?»* или *«Ого, а как вы это построили?»*

3️⃣ Если всё равно не берут – не беда. Разворачивайся и иди к другим. В школе 500 человек, твои люди точно где-то есть! 😉"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=back_to_main())

@bot.callback_query_handler(func=lambda call: call.data == "social_approach")
def social_approach(call):
    text = """😰 *Страшно подойти к компании*

Сердце колотится, ноги ватные, кажется, что все сразу посмотрят? Это адреналин – тело напуганно, но ты сильнее 💪

Сделай простой прием: начни считать про себя. 1... 2... 3... На счёт 5 просто сделай шаг. Один шаг. А там дальше будет легче.

Или подойди не один, а с кем-то. Держаться вдвоём всегда легче. Позови друга и идите вместе знакомиться или проситься в игру 🤝"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=back_to_main())

@bot.callback_query_handler(func=lambda call: call.data == "social_laugh")
def social_laugh(call):
    text = """🙊 *Кажется, что смеются надо мной*

У тебя включился *«микрофон внутреннего критика»* 🎤 Это такой голос в голове, который часто шепчет ерунду. Как его выключить?

Посмотри на компанию и найди 3 доказательства, что они смеются НЕ над тобой. Например: они смотрят в чей-то телефон, показывают друг другу мемы, обсуждают игру, едят бутерброды. Обычно находится куча доказательств, и страх уходит 😌"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=back_to_main())

# ===== 4. ПОССОРИЛСЯ С ДРУГОМ =====
@bot.message_handler(func=lambda m: m.text == "😡 Поссорился с другом")
def fight(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("💬 Да, хочу помириться", callback_data="fight_makeup"),
        types.InlineKeyboardButton("📢 Нет, просто расскажу, что случилось", callback_data="fight_tell")
    )
    text = """😡 *Поссорился с другом*

Обида – как камень в рюкзаке. Тяжело нести, мешает бежать, давит на спину. Хочешь выкинуть этот камень?"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "fight_makeup")
def fight_makeup(call):
    text = """💬 *Как помириться*

Самый крутой способ – *«Я-сообщение»* 💬 Это когда ты говоришь не про другого, а про себя. Сравни:

❌ *Обычная ссора:* «Ты дурак! Ты специально! Ты меня бесишь!» – после этого хочется только драться.

✅ *Я-сообщение:* «МНЕ было обидно, когда ты...» / «Я РАССТРОИЛСЯ, потому что...» / «МНЕ НЕ ПОНРАВИЛОСЬ, что...» – это звучит не как нападение, а как разговор. Попробуешь?

😤 *Если очень зло прямо сейчас — выбери, что поможет:*

🔥 *Методика «Горячие кулаки»:* сожми кулаки изо всех сил, будто хочешь их расплавить. А потом резко РАЗОЖМИ и выдохни. Представь, что из ладоней вылетает горячий пар. Повтори 3 раза – злость уйдёт, а кулаки отдохнут.

✂️ *Методика «Бумажный гнев»:* возьми ненужную бумажку и порви её на мелкие кусочки. Злость уйдет в руки, а не в друга. А завтра поговоришь спокойно ❤️"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=back_to_main())

@bot.callback_query_handler(func=lambda call: call.data == "fight_tell")
def fight_tell(call):
    user_states[call.from_user.id] = "waiting_fight"
    text = """📢 *Расскажи, что случилось*

Рассказывай, я слушаю. Напиши, что случилось (можно голосовым сообщением)."""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "waiting_fight")
def handle_fight(message):
    user_states[message.from_user.id] = None
    text = """💛 *Я тебя услышал*

Знаешь, дружба – это как резинка. Иногда она растягивается, но, если не порвать – возвращается обратно. Дайте друг другу время остыть, а завтра попробуй написать: *«Мир?»* Обычно это работает 💛"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=main_menu())

# ===== 5. УСТАЛ И НИЧЕГО НЕ ХОЧУ =====
@bot.message_handler(func=lambda m: m.text == "😴 Устал и ничего не хочу")
def tired(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Да, готов", callback_data="relax_ready"))
    text = """😴 *Устал и ничего не хочу*

Организм говорит: «Всё, хватит! Давай отдыхать!» Это нормально, даже супергерои берут паузу. Устраивайся поудобнее. Мы сделаем *«Релакс-паузу»* на 5 минут. Готов?"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "relax_ready")
def relax_ready(call):
    text = """🧘 *Релакс-пауза*

Ляг или сядь удобно, закрой глаза. Представь, что ты – мороженое в вафельном стаканчике 🍦 Ты только что из морозилки – твёрдое, холодное, напряжённое.

А теперь солнышко начинает пригревать ☀️ Ты начинаешь таять... руки тают, расслабляются... плечи тают... спина тает... ноги тают...

Ты уже не твёрдое мороженое, а мягкое, тёплое, почти жидкое. Ты растекаешься по стулу... по кровати...

Побудь так минуту. Просто полежи. Ничего не делай. Ни о чем не думай ☁️

А теперь глубокий вдох... потянись... открой глаза и улыбнись 😊

*Как ты? Легче?*"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=back_to_main())

# ===== 6. ПОИГРАЕМ? =====
@bot.message_handler(func=lambda m: m.text == "🎮 Поиграем?")
def games(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📖 Закончи историю", callback_data="game_story"),
        types.InlineKeyboardButton("💪 Собери ресурс", callback_data="game_resource"),
        types.InlineKeyboardButton("😂 Страх-смешилка", callback_data="game_fear")
    )
    text = """🎮 *Поиграем?*

Отлично! Иногда, чтобы успокоиться, нужно просто переключить мозг на что-то другое. Выбирай игру:"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "game_story")
def game_story(call):
    user_states[call.from_user.id] = "waiting_story"
    text = """📖 *Закончи историю*

Я начну историю, а ты придумай смешной или геройский конец. Готов?

*Однажды на контрольной Вася обнаружил, что в его ручке кончилась паста, и он...*

(Напиши свой вариант) 👇"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "game_resource")
def game_resource(call):
    user_states[call.from_user.id] = "waiting_resources"
    text = """💪 *Собери ресурс*

Представь, что твоё спокойствие – это энергия в телефоне 📱 Она садится, когда волнуешься. А заряжается от приятных вещей.

Напиши 3 вещи, которые тебя заряжают: что ты любишь делать, от чего тебе тепло и хорошо? ✨"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "game_fear")
def game_fear(call):
    user_states[call.from_user.id] = "waiting_fear"
    text = """😂 *Страх-смешилка*

Есть секрет: если нарисовать свой страх смешным – он перестаёт пугать 😄 Давай попробуем?

Представь свой страх (ответ у доски, контрольную) и нарисуй его в уме или на бумаге: надень на него смешную шапку 🎩, добавь огромные розовые бантики 🎀, представь, что у него кривые ножки или он танцует ламбаду 💃

А теперь напиши мне одной фразой, какой он получился смешной!"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "waiting_story")
def handle_story(message):
    user_states[message.from_user.id] = None
    text = f"""😄 *Круто!*

А вот как закончил бы эту историю супер-спокойный человек: *«...и он вспомнил, что у него есть запасная ручка в пенале, потому что он всегда готов!»* 

Запасная ручка – наше всё! 📝"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=final_menu())

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "waiting_resources")
def handle_resources(message):
    user_states[message.from_user.id] = None
    text = """✅ *Сохранил!*

Это теперь твой личный список силы. Когда станет грустно – делай что-то из этого списка. Работает лучше конфет! 🍫"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=final_menu())

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "waiting_fear")
def handle_fear(message):
    user_states[message.from_user.id] = None
    text = f"""😂 *Класс!*

Страх в смешной шапке уже не страшный, правда? Запомни этого клоуна и вспоминай, когда снова станет боязно ✨"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=final_menu())

# ===== 7. ПОМОГИ ПРЯМО СЕЙЧАС! =====
@bot.message_handler(func=lambda m: m.text == "🔥 Помоги прямо сейчас!")
def help_now(message):
    user_states[message.from_user.id] = "waiting_see"
    text = """🔥 *Помоги прямо сейчас!*

Стоп. Всё плохо, прямо здесь и сейчас? Дыши. Я рядом. Давай делать *«Якорь»* – это якорь, который удержит тебя в спокойствии ⚓

*1️⃣ Что ты СЕЙЧАС видишь вокруг?* (Напиши 3 вещи) 👀"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "waiting_see")
def handle_see(message):
    user_states[message.from_user.id] = "waiting_hear"
    text = """✅ *Запомнил!*

*2️⃣ Что ты слышишь?* (Напиши 2 звука) 👂"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "waiting_hear")
def handle_hear(message):
    user_states[message.from_user.id] = "waiting_touch"
    text = """✅ *Запомнил!*

*3️⃣ Что ты можешь потрогать рукой прямо сейчас?* (Напиши 1 вещь) ✋"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "waiting_touch")
def handle_touch(message):
    user_states[message.from_user.id] = None
    text = """🧘 *А теперь...*

ВДООООХ (глубокий)... и ВЫЫЫЫДОХ (медленный)...

Ты здесь. Ты в безопасности. Ты справишься. ❤️

*Дыши спокойно. Всё хорошо.*"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=final_menu())

# ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====
def back_to_main():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def final_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("❤️ Что дальше?", callback_data="final_message"))
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main_callback(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "final_message")
def final_message(call):
    text = """❤️ *Помни:*

Ты не один такой. Мы все иногда боимся, злимся или грустим. Это нормально.

Главное – ты молодец, что ищешь помощь и способы справиться.

*Твой друг, Антистресс Гид* ❤️

Возвращайся, если будет трудно!"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=back_to_main())

# ===== ЗАПУСК =====
if __name__ == "__main__":
    # Устанавливаем вебхук
    port = int(os.environ.get('PORT', 10000))
    webhook_url = f"https://antistress-bot-1.onrender.com/webhook" 
    
    print(f"🔗 Устанавливаю вебхук на: {webhook_url}")
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    print("✅ Вебхук установлен")
    
    print(f"🌐 Запускаю Flask на порту {port}")
    app.run(host='0.0.0.0', port=port)
