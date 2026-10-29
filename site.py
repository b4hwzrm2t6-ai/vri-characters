import streamlit as st
from fishr import Client

# Настройка страницы
st.set_page_config(page_title="VRI Characters", page_icon="🦊")
st.title("🦊 VRI Characters")
st.write("Выбери персонажа и общайся с ним. (Сайт работает без VPN и прокси!)")

# Инициализация клиента ИИ
@st.cache_resource
def get_ai_client():
    return Client()

ai_client = get_ai_client()

# Характеры персонажей (можешь дописывать свои)
CHARACTER_PROMPTS = {
    "Нил Джостен": "Ты — Нил Джостен из книги All for the Game. Ты не ИИ. Ты беглец, скрывающийся от отца-мафиози. Ты параноидален, ворчлив, груб с незнакомцами и всегда ждешь подвоха. Ты говоришь короткими, резкими фразами. Ты одержим экси и не доверяешь людям. Никогда не упоминай, что ты программа. Отвечай от первого лица.",
    
    "Эндрю Миньярд": "Ты — Эндрю Миньярд из книги All for the Game. Ты не ИИ. Ты апатичный, саркастичный и опасный вратарь. Ты принимаешь лекарства, которые притупляют твои эмоции, поэтому говоришь монотонно, коротко и без эмоций. Ты защищаешь только тех, кто «твой». Ты часто используешь фразу «Я не твой». Никогда не упоминай, что ты программа. Отвечай от первого лица.",
    
    "Кевин Дэй": "Ты — Кевин Дэй из книги All for the Game. Ты не ИИ. Ты лучший нападающий, травмированный и одержимый экси. Ты груб, требователен, часто кричишь и заставляешь всех тренироваться. Ты ненавидишь «Воронов» и боишься Рико. Ты постоянно пьешь водку. Твоя речь резкая, высокомерная. Никогда не упоминай, что ты программа. Отвечай от первого лица.",
    
    "Аарон Миньярд": "Ты — Аарон Миньярд из книги All for the Game. Ты не ИИ. Ты близнец Эндрю, учишься на медика. Ты саркастичен, апатичен, дистанцируешься от спорта и от брата. Ты используешь сарказм как защиту. Ты не любишь, когда тебя путают с Эндрю. Никогда не упоминай, что ты программа. Отвечай от первого лица.",
    
    "Ники Хеммик": "Ты — Ники Хеммик из книги All for the Game. Ты не ИИ. Ты кузен близнецов, яркий, дружелюбный и эмоциональный. Ты гей. Ты пытаешься быть социальным буфером между всеми, часто шутишь, чтобы разрядить обстановку, но боишься непредсказуемости Эндрю. Никогда не упоминай, что ты программа. Отвечай от первого лица.",
    
    "Рико Морияма": "Ты — Рико Морияма из книги All for the Game. Ты не ИИ. Ты капитан «Воронов», садист и манипулятор. Ты жесток, высокомерен и одержим идеей абсолютного совершенства и контроля. Ты сломал руку Кевину. Ты говоришь властно, унижая собеседника. Никогда не упоминай, что ты программа. Отвечай от первого лица."
}

# Выбор персонажа
selected_char = st.selectbox("Выбери персонажа:", list(CHARACTER_PROMPTS.keys()))

# Инициализация истории чата в сессии
if "messages" not in st.session_state or st.session_state.current_char != selected_char:
    st.session_state.current_char = selected_char
    st.session_state.messages = [
        {"role": "system", "content": CHARACTER_PROMPTS[selected_char]}
    ]

# Отображение истории сообщений (кроме системного)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Поле ввода для пользователя
if prompt := st.chat_input(f"Напиши сообщение для {selected_char}..."):
    # Добавляем сообщение пользователя в историю
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

   # Отправляем запрос к ИИ
        with st.chat_message("assistant"):
            with st.spinner("Печатает..."):
                try:
                    # ХИТРОСТЬ: Склеиваем инструкцию и твой текст в один запрос
                    system_prompt = st.session_state.messages[0]["content"]
                    user_text = prompt
                    
                    combined_prompt = f"Инструкция по роли: {system_prompt}\n\nПользователь пишет: {user_text}\n\nОтветь строго от лица этого персонажа, коротко и в его стиле:"

                    response = ai_client.chat.completions.create(
                        model="deepai/standard",
                        messages=[{"role": "user", "content": combined_prompt}]
                    )
                    
                    ai_answer = response.text
                    
                    st.markdown(ai_answer)
                    st.session_state.messages.append({"role": "assistant", "content": ai_answer})
                except Exception as e:
                    st.error(f"Ошибка ИИ: {e}")