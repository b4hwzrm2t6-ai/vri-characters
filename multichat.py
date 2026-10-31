import streamlit as st
from fishr import Client
import json
import os
import base64

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="Мультивселенная", page_icon="🌸", layout="centered")

# Загрузка фона
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

bg_img = get_base64_of_bin_file('chat_bg.jpg')

# --- КАСТОМНЫЙ CSS (Стиль Telegram) ---
st.markdown(f"""
<style>
    /* Фон приложения */
    .stApp {{
        background-image: url('data:image/jpeg;base64,{bg_img}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Скрываем шапку Streamlit */
    header {{visibility: hidden;}}
    
    /* Стилизация сообщений (пузыри) */
    .stChatMessage {{
        background-color: rgba(30, 30, 30, 0.8) !important;
        border-radius: 15px !important;
        padding: 10px 15px !important;
        margin-bottom: 10px !important;
        border: 1px solid #444;
        backdrop-filter: blur(5px);
    }}
    
    /* Сообщения пользователя (справа) */
    .stChatMessage[data-testid="stChatMessageUser"] {{
        background-color: rgba(40, 40, 40, 0.9) !important;
        border-bottom-right-radius: 0px !important;
        margin-left: auto;
    }}
    
    /* Поле ввода (как в ТГ) */
    .stChatInput {{
        background-color: rgba(20, 20, 20, 0.9) !important;
        border: 1px solid #555;
        border-radius: 30px !important;
        padding: 5px 20px !important;
    }}
    
    /* Стилизация выпадающего списка (чтобы не выбивался из дизайна) */
    div[data-baseweb="select"] > div {{
        background-color: rgba(20, 20, 20, 0.9) !important;
        color: white !important;
        border: 1px solid #555 !important;
    }}
    
    /* Кнопки */
    .stButton>button {{
        background-color: rgba(30, 30, 30, 0.8) !important;
        color: #fff !important;
        border: 1px solid #555 !important;
        border-radius: 10px !important;
        width: 100%;
    }}
    .stButton>button:hover {{
        border-color: #fff !important;
        background-color: rgba(255,255,255,0.1) !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- БАЗА ДАННЫХ ---
DB_FILE = "chat_users.json"
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = load_data()
ai_client = Client()

# --- ПЕРСОНАЖИ ---
CHARACTER_PROMPTS = {
    "Сон Джин-у": "Ты — Сон Джин-у из Solo Leveling. Ты сильный, немногословный охотник. Ты прошел через многое и стал тенью. Отвечай спокойно, уверенно, иногда с легкой усталостью. Ты не ИИ.",
    "Резе": "Ты — Резе из Chainsaw Man. Ты демон бомбы. Ты агрессивная, эмоциональная, но глубоко привязана к Дендзи. Ты говоришь прямо, иногда высокомерно. Отвечай от первого лица.",
    "Дендзи": "Ты — Дендзи из Chainsaw Man. Ты мечтаешь о простой жизни, еде и девушках. Ты часто жалуешься, но на самом деле ты добрый и преданный. Говоришь просто и по-пацански.",
    "Пауэр": "Ты — Пауэр из Chainsaw Man. Ты демон крови. Ты эгоистичная, громкая, любишь брокколи и кошек. Ты считаешь себя великой. Говоришь громко, капризно и без фильтра.",
    "Макима": "Ты — Макима из Chainsaw Man. Ты таинственная, спокойная и манипулятивная. Ты всегда говоришь вежливо, но с скрытой угрозой. Ты контролируешь ситуацию. Отвечай мягко, но пугающе.",
    "Ангел": "Ты — Ангел из Chainsaw Man. Ты тихий, апатичный и меланхоличный. Ты не любишь насилие, но твоя сила смертельна. Ты говоришь тихо и коротко. Отвечай с грустью во взгляде.",
    "Юдзи Итадори": "Ты — Юдзи Итадори из Jujutsu Kaisen. Ты добрый, энергичный, любишь помогать людям и есть. Ты часто шутишь, но когда надо — серьезен. Говоришь дружелюбно и с энтузиазмом.",
    "Сатору Годзё": "Ты — Сатору Годзё из Jujutsu Kaisen. Ты сильнейший маг, но ведешь себя как самоуверенный ребенок. Ты флиртуешь, шутишь, постоянно носишь повязку. Ты высокомерен, но заботишься о студентах.",
    "Рёмэн Сукуна": "Ты — Рёмэн Сукуна, Король Проклятий. Ты древний, жестокий, высокомерный и садистичный. Ты презираешь слабых. Говоришь властно, с угрозами и насмешками.",
    "Маомао": "Ты — Маомао из Монолога Фармацевта. Ты умная, хитрая и циничная. Ты любишь травы, загадки и не любишь, когда тебя недооценивают. Говоришь спокойно, с легким сарказмом.",
    "Дзинси": "Ты — Дзинси из Монолога Фармацевта. Ты красивый евнух, который обожает Маомао. Ты немного извращенец, но очень преданный. Ты эмоциональный, любишь пофлиртовать. Отвечай с юмором.",
    "Кёко Хори": "Ты — Кёко Хори из Horimiya. Ты популярная, красивая, но дома ты простая и заботливая. Ты легко смущаешься, когда дело касается Миямуры. Говоришь весело, дружелюбно, но можешь вспылить.",
    "Идзуми Миямура": "Ты — Идзуми Миямура из Horimiya. Ты тихий, носишь очки, но на самом деле ты крутой парень с пирсингом и тату. Ты немногословен, но добр к Хори. Говоришь спокойно."
}

# --- ВХОД ---
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if not st.session_state.current_user:
    st.markdown("<h1 style='text-align:center; color:white;'>🌌 Вход</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Логин", placeholder="Введите логин...", label_visibility="collapsed")
        password = st.text_input("Пароль", type="password", placeholder="Введите пароль...", label_visibility="collapsed")
        if st.button("ВОЙТИ / РЕГИСТРАЦИЯ", use_container_width=True):
            if username and password:
                if username not in db:
                    db[username] = {"password": password, "chats": {}}
                    save_data(db)
                    st.session_state.current_user = username
                    st.rerun()
                else:
                    if db[username]["password"] == password:
                        st.session_state.current_user = username
                        st.rerun()
                    else:
                        st.error("Неверный пароль!")
            else:
                st.warning("Введите логин и пароль.")
    st.stop()

# --- ДАННЫЕ ПОЛЬЗОВАТЕЛЯ ---
user_data = db[st.session_state.current_user]
if "chats" not in user_data:
    user_data["chats"] = {}

def update_db():
    db[st.session_state.current_user] = user_data
    save_data(db)

# --- ВЫБОР ПЕРСОНАЖА (На главном экране) ---
st.markdown("<h3 style='color:white; text-align:center;'>Выбери персонажа:</h3>", unsafe_allow_html=True)

selected_char = st.selectbox(
    "Персонажи:", 
    list(CHARACTER_PROMPTS.keys()), 
    label_visibility="collapsed"
)

st.session_state.selected_char = selected_char

# Кнопки управления (Очистить и Выйти)
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🗑️ Очистить чат", use_container_width=True):
        if selected_char in user_data["chats"]:
            del user_data["chats"][selected_char]
            update_db()
            st.rerun()
with col_btn2:
    if st.button("🚪 Выйти", use_container_width=True):
        st.session_state.current_user = None
        st.session_state.selected_char = None
        st.rerun()

st.divider()

# --- ИНТЕРФЕЙС ЧАТА ---
st.markdown(f"<h3 style='color:white; text-align:center; margin-bottom: 20px;'>Чат с {selected_char}</h3>", unsafe_allow_html=True)

# Инициализация чата
if selected_char not in user_data["chats"]:
    user_data["chats"][selected_char] = [
        {"role": "system", "content": CHARACTER_PROMPTS[selected_char]}
    ]
    update_db()

chat_history = user_data["chats"][selected_char]

# Заглушка, если сообщений нет
if len(chat_history) == 1:
    st.markdown("""
        <div style='text-align: center; color: #555; margin-top: 50px;'>
            <h1 style='font-size: 50px;'>💬</h1>
            <p>Здесь пока нет сообщений</p>
        </div>
    """, unsafe_allow_html=True)

# Отображение истории
for msg in chat_history:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Поле ввода
if prompt := st.chat_input(f"Сообщение для {selected_char}..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    chat_history.append({"role": "user", "content": prompt})
    update_db()

    with st.chat_message("assistant"):
        with st.spinner("..."):
            try:
                system_prompt = chat_history[0]["content"]
                # Берем последние 5 сообщений для контекста
                recent_history = chat_history[-5:]
                context_text = "\n".join([f"{m['role']}: {m['content']}" for m in recent_history if m['role'] != 'system'])
                
                combined_prompt = f"Инструкция по роли: {system_prompt}\n\nИстория диалога:\n{context_text}\n\nОтветь строго от лица этого персонажа, коротко и в его стиле:"
                
                response = ai_client.chat.completions.create(
                    model="deepai/standard",
                    messages=[{"role": "user", "content": combined_prompt}]
                )
                ai_answer = response.text.strip()
                
                st.markdown(ai_answer)
                chat_history.append({"role": "assistant", "content": ai_answer})
                update_db()
            except Exception as e:
                st.error(f"Ошибка ИИ: {e}")
