import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Моя Белка", page_icon="🐿️", layout="centered")

# --- МОЩНЫЙ ИНТЕРАКТИВНЫЙ КОД ---
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #222;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        /* Игровое поле */
        #game {
            position: relative;
            width: 100%;
            max-width: 600px;
            height: 600px;
            background: linear-gradient(to bottom, #6dd5ed, #2193b0); /* День */
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            overflow: hidden;
            transition: background 2s;
        }
        
        /* Ночь */
        #game.night {
            background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        }

        /* Белка */
        #squirrel {
            position: absolute;
            bottom: 100px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 120px;
            cursor: pointer;
            transition: transform 0.2s;
            animation: breathe 3s infinite ease-in-out;
            z-index: 10;
        }
        
        #squirrel.sleeping {
            font-size: 100px;
            opacity: 0.8;
            animation: none;
        }

        /* Анимация дыхания */
        @keyframes breathe {
            0%, 100% { transform: translateX(-50%) scale(1); }
            50% { transform: translateX(-50%) scale(1.05); }
        }

        /* Пузырь с эмоцией */
        #bubble {
            position: absolute;
            top: 150px;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 15px 25px;
            border-radius: 30px;
            font-size: 20px;
            font-weight: bold;
            color: #333;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 20;
        }
        
        #bubble:after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            border-width: 10px 10px 0;
            border-style: solid;
            border-color: white transparent;
        }

        /* Шкалы */
        #ui {
            position: absolute;
            top: 20px;
            left: 20px;
            width: 250px;
            background: rgba(255,255,255,0.9);
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            z-index: 20;
        }
        .bar-container { margin-bottom: 10px; }
        .bar-label { font-size: 14px; font-weight: bold; color: #444; display: flex; justify-content: space-between;}
        .bar-bg { width: 100%; height: 12px; background: #ddd; border-radius: 10px; overflow: hidden; margin-top: 3px;}
        .bar-fill { height: 100%; transition: width 0.3s, background-color 0.3s; }
        #fill-food { background: #ff9800; width: 100%; }
        #fill-happy { background: #e91e63; width: 100%; }
        #fill-clean { background: #00bcd4; width: 100%; }

        /* Кнопки */
        #controls {
            position: absolute;
            bottom: 0;
            width: 100%;
            display: flex;
            justify-content: space-around;
            background: rgba(0,0,0,0.6);
            padding: 20px 0;
            z-index: 20;
        }
        
        .action-btn {
            background: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 30px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            transition: transform 0.1s;
        }
        .action-btn:active { transform: scale(0.9); }
        .action-btn:disabled { opacity: 0.5; cursor: not-allowed; }

        /* Эффекты */
        .floating-item {
            position: absolute;
            font-size: 40px;
            animation: flyUp 1s forwards;
            pointer-events: none;
            z-index: 15;
        }
        @keyframes flyUp {
            0% { transform: translateY(0) scale(1); opacity: 1; }
            100% { transform: translateY(-150px) scale(1.5); opacity: 0; }
        }
    </style>
</head>
<body>

<div id="game">
    <div id="ui">
        <div class="bar-container">
            <div class="bar-label"><span>🍎 Сытость</span> <span id="val-food">100</span></div>
            <div class="bar-bg"><div class="bar-fill" id="fill-food"></div></div>
        </div>
        <div class="bar-container">
            <div class="bar-label"><span>🎾 Настроение</span> <span id="val-happy">100</span></div>
            <div class="bar-bg"><div class="bar-fill" id="fill-happy"></div></div>
        </div>
        <div class="bar-container">
            <div class="bar-label"><span>🧼 Чистота</span> <span id="val-clean">100</span></div>
            <div class="bar-bg"><div class="bar-fill" id="fill-clean"></div></div>
        </div>
    </div>

    <div id="bubble">Привет! Я Белочка! 🐿️</div>
    <div id="squirrel">🐿️</div>

    <div id="controls">
        <button class="action-btn" onclick="doAction('feed')" title="Покормить">🌰</button>
        <button class="action-btn" onclick="doAction('play')" title="Поиграть">🎾</button>
        <button class="action-btn" onclick="doAction('clean')" title="Помыть">🧼</button>
        <button class="action-btn" onclick="doAction('sleep')" title="Спать">💤</button>
    </div>
</div>

<script>
    // Состояние белки
    let state = {
        food: 100,
        happy: 100,
        clean: 100,
        isSleeping: false
    };

    const game = document.getElementById('game');
    const squirrel = document.getElementById('squirrel');
    const bubble = document.getElementById('bubble');

    // Показать сообщение
    function say(text) {
        bubble.innerText = text;
        bubble.style.opacity = 1;
        clearTimeout(window.bubbleTimer);
        window.bubbleTimer = setTimeout(() => { bubble.style.opacity = 0; }, 3000);
    }

    // Эффект при действии
    function spawnEffect(x, y, emoji) {
        const el = document.createElement('div');
        el.className = 'floating-item';
        el.innerText = emoji;
        el.style.left = x + 'px';
        el.style.top = y + 'px';
        game.appendChild(el);
        setTimeout(() => el.remove(), 1000);
    }

    // Обновление интерфейса
    function updateUI() {
        // Ограничиваем от 0 до 100
        state.food = Math.min(100, Math.max(0, state.food));
        state.happy = Math.min(100, Math.max(0, state.happy));
        state.clean = Math.min(100, Math.max(0, state.clean));

        document.getElementById('val-food').innerText = Math.round(state.food);
        document.getElementById('val-happy').innerText = Math.round(state.happy);
        document.getElementById('val-clean').innerText = Math.round(state.clean);

        document.getElementById('fill-food').style.width = state.food + '%';
        document.getElementById('fill-happy').style.width = state.happy + '%';
        document.getElementById('fill-clean').style.width = state.clean + '%';

        // Цвета при плохом состоянии
        document.getElementById('fill-food').style.backgroundColor = state.food < 30 ? '#f44336' : '#ff9800';
        document.getElementById('fill-happy').style.backgroundColor = state.happy < 30 ? '#f44336' : '#e91e63';
        document.getElementById('fill-clean').style.backgroundColor = state.clean < 30 ? '#f44336' : '#00bcd4';
    }

    // Действия
    function doAction(type) {
        if (state.isSleeping && type !== 'sleep') {
            say('Zzz... Я сплю, не мешай...');
            return;
        }

        const rect = squirrel.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        if (type === 'feed') {
            state.food = Math.min(100, state.food + 20);
            say('Ням-ням! 🥰');
            spawnEffect(centerX, centerY, '❤️');
        } 
        else if (type === 'play') {
            state.happy = Math.min(100, state.happy + 25);
            state.food = Math.max(0, state.food - 10); // Тратит энергию
            say('Ура! Догоняй! 🎾');
            spawnEffect(centerX, centerY, '✨');
        }
        else if (type === 'clean') {
            state.clean = 100;
            say('Блеск! Я самая чистая белка! 🧼');
            spawnEffect(centerX, centerY, '🫧');
        }
        else if (type === 'sleep') {
            state.isSleeping = !state.isSleeping;
            if (state.isSleeping) {
                squirrel.classList.add('sleeping');
                squirrel.innerText = '😴';
                say('Спокойной ночи... 💤');
                game.classList.add('night');
            } else {
                squirrel.classList.remove('sleeping');
                squirrel.innerText = '🐿️';
                say('Выспалась! Что будем делать?');
                game.classList.remove('night');
            }
        }
        updateUI();
    }

    // Постепенное уменьшение статов (каждые 3 секунды)
    setInterval(() => {
        if (!state.isSleeping) {
            state.food -= 2;
            state.happy -= 1;
            state.clean -= 1;
            
            // Если голодная или грязная - говорит об этом
            if (Math.random() < 0.1) { // 10% шанс
                if (state.food < 30) say('Я голодная... 🥺');
                else if (state.clean < 30) say('Я грязная, помоги мне! 🧼');
                else if (state.happy < 30) say('Мне скучно... поиграй со мной.');
            }
        } else {
            // Восстановление энергии во сне
            state.food -= 0.5;
        }
        updateUI();
    }, 3000);

    // Погладить белку (клик по ней)
    squirrel.addEventListener('click', () => {
        if (!state.isSleeping) {
            state.happy = Math.min(100, state.happy + 5);
            say('Хи-хи, щекотно! 🥰');
            const rect = squirrel.getBoundingClientRect();
            spawnEffect(rect.left + rect.width/2, rect.top, '💖');
            updateUI();
        }
    });

</script>
</body>
</html>
"""

# Отображаем игру
components.html(game_html, height=620)