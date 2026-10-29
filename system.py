import streamlit as st
from fishr import Client
import random

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="SYSTEM", page_icon="⚠️", layout="centered")

# --- КАСТОМНЫЙ CSS (Стиль Соло Левелинга) ---
st.markdown("""
<style>
    .stApp {
        background-color: #0a0b10;
        color: #8ab4f8;
    }
    .system-box {
        background: rgba(10, 25, 50, 0.7);
        border: 2px solid #4da6ff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 0 15px #4da6ff, inset 0 0 15px #4da6ff;
        margin-bottom: 20px;
        transition: all 0.5s ease;
    }
    .system-title {
        color: #4da6ff;
        text-align: center;
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stat-name {
        color: #8ab4f8;
        font-weight: bold;
    }
    .stat-value {
        color: #ffffff;
        font-size: 20px;
        float: right;
    }
    .stButton>button {
        background-color: transparent;
        color: #4da6ff;
        border: 1px solid #4da6ff;
        border-radius: 5px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #4da6ff;
        color: #0a0b10;
        box-shadow: 0 0 10px #4da6ff;
    }
</style>
""", unsafe_allow_html=True)

# --- ИНИЦИАЛИЗАЦИЯ ПАМЯТИ ИГРЫ ---
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.exp = 0
    st.session_state.max_exp = 100
    st.session_state.stats = {"Сила": 10, "Ловкость": 10, "Интеллект": 10, "Выносливость": 10}
    st.session_state.points = 0
    st.session_state.quest = None

ai_client = Client()

# --- СИСТЕМА РАНГОВ ---
def get_rank(level):
    if level < 5: return "E", "#8ab4f8", "серый"
    elif level < 10: return "D", "#4da6ff", "синий"
    elif level < 15: return "C", "#00ffcc", "бирюзовый"
    elif level < 20: return "B", "#b366ff", "фиолетовый"
    elif level < 30: return "A", "#ffcc00", "золотой"
    elif level < 50: return "S", "#ff3333", "красный"
    else: return "N", "#ffffff", "белый (Национальный)"

rank, color, rank_color_name = get_rank(st.session_state.level)

# --- ИНТЕРФЕЙС ---
st.markdown(f"<h1 class='system-title' style='color: {color}; text-shadow: 0 0 10px {color};'>⚠️ Система активирована ⚠️</h1>", unsafe_allow_html=True)

st.markdown(f"""
<div class='system-box' style='border-color: {color}; box-shadow: 0 0 15px {color}, inset 0 0 15px {color};'>
    <h2 class='system-title' style='color: {color};'>Статус</h2>
    <p class='stat-name'>Ранг: <span class='stat-value' style='color: {color}; font-weight: bold; text-shadow: 0 0 5px {color};'>{rank}-Ранг</span></p>
    <p class='stat-name'>Уровень: <span class='stat-value'>{st.session_state.level}</span></p>
    <p class='stat-name'>Опыт: <span class='stat-value'>{st.session_state.exp} / {st.session_state.max_exp}</span></p>
    <p class='stat-name'>Свободные очки: <span class='stat-value'>{st.session_state.points}</span></p>
    <hr style='border-color: {color}; opacity: 0.5;'>
    <p class='stat-name'>Сила: <span class='stat-value'>{st.session_state.stats['Сила']}</span></p>
    <p class='stat-name'>Ловкость: <span class='stat-value'>{st.session_state.stats['Ловкость']}</span></p>
    <p class='stat-name'>Интеллект: <span class='stat-value'>{st.session_state.stats['Интеллект']}</span></p>
    <p class='stat-name'>Выносливость: <span class='stat-value'>{st.session_state.stats['Выносливость']}</span></p>
</div>
""", unsafe_allow_html=True)

# Функция добавления опыта
def add_exp(amount):
    old_level = st.session_state.level
    st.session_state.exp += amount
    while st.session_state.exp >= st.session_state.max_exp:
        st.session_state.exp -= st.session_state.max_exp
        st.session_state.level += 1
        st.session_state.max_exp = int(st.session_state.max_exp * 1.5)
        st.session_state.points += 5
        
        new_rank, _, _ = get_rank(st.session_state.level)
        old_rank, _, _ = get_rank(old_level)
        
        if new_rank != old_rank:
            st.success(f"🚨 ВНИМАНИЕ! Ваш ранг повышен до {new_rank}!")
        st.success(f"🎉 УРОВЕНЬ ПОВЫШЕН! Теперь у тебя {st.session_state.level} уровень. Получено 5 очков характеристик!")

# --- ПРОКАЧКА ХАРАКТЕРИСТИК ---
st.markdown("<h3 class='system-title'>Повседневные задания</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    if st.button("💪 Отжаться 50 раз (+15 опыта)"):
        add_exp(15)
        st.rerun()
    if st.button("🧠 Прочитать 10 страниц (+10 опыта)"):
        add_exp(10)
        st.rerun()

with col2:
    if st.button("🏃 Пробежать 3 км (+20 опыта)"):
        add_exp(20)
        st.rerun()
    if st.button("🧘 Помедитировать 10 минут (+5 опыта)"):
        add_exp(5)
        st.rerun()

# --- ГЕНЕРАЦИЯ КВЕСТОВ ---
st.markdown("<h3 class='system-title'>Ежедневный квест</h3>", unsafe_allow_html=True)

if st.button("Сгенерировать квест"):
    with st.spinner("Система генерирует задание..."):
        try:
            response = ai_client.chat.completions.create(
                model="deepai/standard",
                messages=[{"role": "user", "content": f"Ты - Система из аниме Solo Leveling. Игрок {rank}-ранга. Придумай мне один короткий ежедневный квест на русском языке (например: отжаться 100 раз, выучить 10 новых слов, убраться в комнате). Напиши только название квеста и награду в опыте (от 10 до 30). Сделай текст коротким и командным тоном."}]
            )
            st.session_state.quest = response.text
        except Exception as e:
            st.error(f"Ошибка генерации: {e}")

if st.session_state.quest:
    st.markdown(f"""
    <div class='system-box' style='border-color: #ffcc00; box-shadow: 0 0 15px #ffcc00;'>
        <h3 class='system-title' style='color: #ffcc00;'>Новый квест!</h3>
        <p style='color: #ffffff; font-size: 18px;'>{st.session_state.quest}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✅ Квест выполнен! Забрать награду"):
        add_exp(20) 
        st.session_state.quest = None
        st.rerun()

# --- РАСПРЕДЕЛЕНИЕ ОЧКОВ ---
if st.session_state.points > 0:
    st.markdown("<h3 class='system-title'>Распределение очков</h3>", unsafe_allow_html=True)
    stat_to_up = st.selectbox("Куда вложить очки?", list(st.session_state.stats.keys()))
    if st.button("Увеличить характеристику"):
        st.session_state.stats[stat_to_up] += 1
        st.session_state.points -= 1
        st.rerun() 