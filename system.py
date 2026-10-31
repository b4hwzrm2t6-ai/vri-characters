import streamlit as st
from fishr import Client
import json
import os
import base64

st.set_page_config(page_title="SYSTEM", page_icon="⚠️", layout="centered")

# Фон
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    bg_img = get_base64_of_bin_file('bg.jpg')
    bg_css = f"background-image: url('data:image/jpeg;base64,{bg_img}'); background-size: cover; background-position: center;"
except:
    bg_css = "background-color: #050510;"

# --- КАСТОМНЫЙ CSS БЕЗ HTML-ТЕГОВ В ТЕКСТЕ ---
st.markdown(f"""
<style>
    .stApp {{ {bg_css} }}
    header {{visibility: hidden;}}
    
    /* Стилизация контейнеров Streamlit под окно Системы */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(5, 10, 30, 0.85) !important;
        border: 2px solid #4da6ff !important;
        border-radius: 5px !important;
        box-shadow: 0 0 20px #4da6ff, inset 0 0 20px #4da6ff !important;
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
    }}
    
    h1, h2, h3, p, span, div {{
        font-family: 'Courier New', monospace !important;
        color: #8ab4f8;
    }}
    
    .big-title {{
        color: #ffffff !important;
        text-align: center;
        font-size: 32px !important;
        letter-spacing: 5px;
        text-shadow: 0 0 10px #4da6ff, 0 0 20px #4da6ff;
    }}
    
    /* Кнопки */
    .stButton>button {{
        background-color: rgba(10, 25, 50, 0.8) !important;
        color: #4da6ff !important;
        border: 1px solid #4da6ff !important;
        border-radius: 0px !important;
        width: 100%;
        font-family: 'Courier New', monospace !important;
    }}
    .stButton>button:hover {{
        background-color: #4da6ff !important;
        color: #000 !important;
        box-shadow: 0 0 15px #4da6ff !important;
    }}
    
    /* Поля ввода */
    .stTextInput>div>div>input {{
        background-color: rgba(10, 25, 50, 0.8) !important;
        color: white !important;
        border: 1px solid #4da6ff !important;
        border-radius: 0px !important;
    }}
</style>
""", unsafe_allow_html=True)

ai_client = Client()

# --- БАЗА ДАННЫХ ---
DB_FILE = "users_data.json"
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = load_data()

# --- ВХОД ---
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if not st.session_state.current_user:
    st.markdown("<h2 class='big-title' style='margin-top: 50px;'>ДОСТУП К СИСТЕМЕ</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Логин", placeholder="Введите логин...", label_visibility="collapsed")
        password = st.text_input("Пароль", type="password", placeholder="Введите пароль...", label_visibility="collapsed")
        if st.button("ВОЙТИ / РЕГИСТРАЦИЯ"):
            if username and password:
                if username not in db:
                    db[username] = {
                        "password": password, "level": 1, "exp": 0, "max_exp": 100, "points": 0,
                        "stats": {"Сила": 10, "Выносливость": 10, "Ловкость": 10, "Интеллект": 10}, "quest": None
                    }
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

# --- ЛОГИКА ---
user_data = db[st.session_state.current_user]
def update_db():
    db[st.session_state.current_user] = user_data
    save_data(db)

def get_rank(level):
    if level < 5: return "E", "#4da6ff"
    elif level < 10: return "D", "#00e5ff"
    elif level < 15: return "C", "#00ffaa"
    elif level < 20: return "B", "#b366ff"
    elif level < 30: return "A", "#ffcc00"
    elif level < 50: return "S", "#ff3333"
    else: return "N", "#ffffff"

rank_letter, rank_color = get_rank(user_data['level'])

def add_exp(amount):
    old_rank, _ = get_rank(user_data['level'])
    user_data['exp'] += amount
    while user_data['exp'] >= user_data['max_exp']:
        user_data['exp'] -= user_data['max_exp']
        user_data['level'] += 1
        user_data['max_exp'] = int(user_data['max_exp'] * 1.5)
        user_data['points'] += 5
        new_rank, _ = get_rank(user_data['level'])
        if new_rank != old_rank:
            st.toast(f"🚨 РАНГ ПОВЫШЕН ДО {new_rank}!", icon="⚠️")
        st.toast(f"🎉 УРОВЕНЬ {user_data['level']}!", icon="✨")
    update_db()

# --- ГЛАВНОЕ ОКНО (Используем st.container с рамкой) ---
with st.container(border=True):
    st.markdown("<h1 class='big-title'>СИСТЕМА</h1>", unsafe_allow_html=True)
    
    st.info("**Поздравляем!**\nВы активировали систему.\nТеперь вы можете получать задания, повышать уровень и становиться сильнее.")
    
    c1, c2 = st.columns([3, 1])
    with c1:
        st.write(f"👤 **Уровень:** {user_data['level']}")
        st.write(f"Опыт: {user_data['exp']} / {user_data['max_exp']}")
        st.write(f"Свободные очки: {user_data['points']}")
    with c2:
        st.markdown(f"<div style='text-align:center; border: 2px solid {rank_color}; box-shadow: 0 0 10px {rank_color}; padding:10px;'>"
                    f"<div style='font-size:10px;'>РАНГ</div>"
                    f"<div style='font-size:40px; color:{rank_color}; font-weight:bold;'>{rank_letter}</div>"
                    f"<div style='font-size:10px;'>{rank_letter}-РАНГ</div></div>", unsafe_allow_html=True)
    
    st.divider()
    st.write("**Характеристики:**")
    st.write(f"❤️ Сила: {user_data['stats']['Сила']}")
    st.write(f"🛡️ Выносливость: {user_data['stats']['Выносливость']}")
    st.write(f"⚡ Ловкость: {user_data['stats']['Ловкость']}")
    st.write(f"🧠 Интеллект: {user_data['stats']['Интеллект']}")
    
    st.divider()
    st.warning(f"**Текущее задание:**\n{user_data['quest'] if user_data['quest'] else 'Выжить и стать сильнее.'}")

# --- УПРАВЛЕНИЕ ---
st.write("")
if st.button("Выйти из аккаунта"):
    st.session_state.current_user = None
    st.rerun()

st.write("### Повседневные задания")
c1, c2 = st.columns(2)
with c1:
    if st.button("💪 Отжаться 50 раз (+15)"): add_exp(15); st.rerun()
    if st.button("🧠 Прочитать 10 страниц (+10)"): add_exp(10); st.rerun()
with c2:
    if st.button("🏃 Пробежать 3 км (+20)"): add_exp(20); st.rerun()
    if st.button("🧘 Помедитировать (+5)"): add_exp(5); st.rerun()

if user_data['points'] > 0:
    st.write(f"### Свободные очки: {user_data['points']}")
    c_stat, c_btn = st.columns([2,1])
    with c_stat:
        stat_up = st.selectbox("Выберите характеристику:", list(user_data['stats'].keys()), label_visibility="collapsed")
    with c_btn:
        if st.button("Увеличить"):
            user_data['stats'][stat_up] += 1
            user_data['points'] -= 1
            update_db()
            st.rerun()

st.write("### Генератор квестов")
if st.button("⚠️ ПОЛУЧИТЬ НОВОЕ ЗАДАНИЕ"):
    with st.spinner("Связь с системой..."):
        try:
            prompt = f"Ты — Система из Solo Leveling. Игрок {rank_letter}-ранга. Придумай ОДИН реальный и выполнимый квест. Категории: спорт, учеба, быт. Формат: 'Задание: [действие с цифрами]. Награда: [число] опыта.'"
            response = ai_client.chat.completions.create(
                model="deepai/standard",
                messages=[{"role": "user", "content": prompt}]
            )
            user_data['quest'] = response.text.strip()
            update_db()
            st.rerun()
        except Exception as e:
            st.error(f"Ошибка: {e}")
            
if user_data['quest']:
    if st.button("✅ ЗАДАНИЕ ВЫПОЛНЕНО (+20 ОПЫТА)"):
        add_exp(20)
        user_data['quest'] = None
        update_db()
        st.rerun()
