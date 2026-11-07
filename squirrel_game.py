import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Моя Белка", page_icon="🐿️", layout="centered")

# Этот HTML-код создает полноценную игру прямо внутри Streamlit
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #2e1a0f;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            width: 100%;
            height: 600px;
            background: linear-gradient(to bottom, #87CEEB 0%, #228B22 100%);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        /* Лесной фон */
        .tree {
            position: absolute;
            bottom: 50px;
            width: 40px;
            height: 200px;
            background-color: #5c4033;
            border-radius: 10px;
        }
        .leaves {
            position: absolute;
            bottom: 150px;
            width: 100px;
            height: 100px;
            background-color: #228B22;
            border-radius: 50%;
            left: -30px;
        }
        
        /* Белка */
        #squirrel {
            position: absolute;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 80px;
            cursor: pointer;
            transition: transform 0.2s;
            user-select: none;
        }
        #squirrel:active {
            transform: translateX(-50%) scale(0.9);
        }
        
        /* Инвентарь */
        #inventory {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 80px;
            background-color: rgba(0,0,0,0.6);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            border-top: 3px solid #ffb6c1;
        }
        .item {
            font-size: 40px;
            cursor: grab;
            user-select: none;
            transition: transform 0.1s;
        }
        .item:active {
            cursor: grabbing;
            transform: scale(1.2);
        }
        
        /* Шкалы */
        #stats {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255,255,255,0.8);
            padding: 10px;
            border-radius: 10px;
            width: 200px;
        }
        .stat-bar {
            width: 100%;
            height: 15px;
            background: #ddd;
            border-radius: 10px;
            margin-bottom: 5px;
            overflow: hidden;
        }
        .fill {
            height: 100%;
            width: 100%;
            transition: width 0.3s;
        }
        #hunger-fill { background-color: #ff4d4d; }
        #happy-fill { background-color: #4da6ff; }
        
        /* Эффекты */
        .heart {
            position: absolute;
            font-size: 30px;
            animation: floatUp 1s forwards;
            pointer-events: none;
        }
        @keyframes floatUp {
            0% { opacity: 1; transform: translateY(0); }
            100% { opacity: 0; transform: translateY(-100px); }
        }
    </style>
</head>
<body>

<div id="game-container">
    <!-- Деревья -->
    <div class="tree" style="left: 50px;"><div class="leaves"></div></div>
    <div class="tree" style="right: 50px;"><div class="leaves"></div></div>
    
    <!-- Шкалы -->
    <div id="stats">
        <div>🍎 Сытость</div>
        <div class="stat-bar"><div class="fill" id="hunger-fill" style="width: 50%;"></div></div>
        <div>🎾 Настроение</div>
        <div class="stat-bar"><div class="fill" id="happy-fill" style="width: 50%;"></div></div>
    </div>

    <!-- Белка -->
    <div id="squirrel">🐿️</div>

    <!-- Инвентарь -->
    <div id="inventory">
        <div class="item" draggable="true" data-type="food" data-value="20" data-emoji="🌰">🌰</div>
        <div class="item" draggable="true" data-type="food" data-value="15" data-emoji="🍎">🍎</div>
        <div class="item" draggable="true" data-type="toy" data-value="20" data-emoji="🎾">🎾</div>
        <div class="item" draggable="true" data-type="toy" data-value="25" data-emoji="🧸">🧸</div>
    </div>
</div>

<script>
    let hunger = 50;
    let happiness = 50;
    
    const squirrel = document.getElementById('squirrel');
    const hungerFill = document.getElementById('hunger-fill');
    const happyFill = document.getElementById('happy-fill');
    const container = document.getElementById('game-container');

    // Обновление шкал
    function updateStats() {
        hunger = Math.min(100, Math.max(0, hunger));
        happiness = Math.min(100, Math.max(0, happiness));
        
        hungerFill.style.width = hunger + '%';
        happyFill.style.width = happiness + '%';
    }

    // Эффект сердечек
    function spawnHeart(x, y, emoji) {
        const heart = document.createElement('div');
        heart.className = 'heart';
        heart.innerText = emoji;
        heart.style.left = x + 'px';
        heart.style.top = y + 'px';
        container.appendChild(heart);
        setTimeout(() => heart.remove(), 1000);
    }

    // --- ЛОГИКА DRAG AND DROP ---
    const items = document.querySelectorAll('.item');
    
    items.forEach(item => {
        item.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('type', item.dataset.type);
            e.dataTransfer.setData('value', item.dataset.value);
            e.dataTransfer.setData('emoji', item.dataset.emoji);
        });
    });

    // Разрешаем бросать предметы на контейнер
    container.addEventListener('dragover', (e) => {
        e.preventDefault(); // Обязательно для работы drop
    });

    container.addEventListener('drop', (e) => {
        e.preventDefault();
        const type = e.dataTransfer.getData('type');
        const value = parseInt(e.dataTransfer.getData('value'));
        const emoji = e.dataTransfer.getData('emoji');
        
        // Проверяем, попали ли мы по белке (хотя бы примерно по центру)
        const rect = squirrel.getBoundingClientRect();
        const x = e.clientX;
        const y = e.clientY;
        
        // Если бросок был рядом с белкой (в радиусе 150 пикселей)
        if (x > rect.left - 50 && x < rect.right + 50 && y > rect.top - 50 && y < rect.bottom + 50) {
            
            if (type === 'food') {
                hunger += value;
                squirrel.innerText = '😋'; // Белка жует
                setTimeout(() => squirrel.innerText = '🐿️', 1000);
                spawnHeart(x, y, '❤️');
            } else if (type === 'toy') {
                happiness += value;
                squirrel.innerText = '🥳'; // Белка радуется
                setTimeout(() => squirrel.innerText = '🐿️', 1000);
                spawnHeart(x, y, '✨');
            }
            
            updateStats();
        }
    });
    
    // Постепенное уменьшение статов (каждые 5 секунд)
    setInterval(() => {
        hunger -= 1;
        happiness -= 1;
        updateStats();
    }, 5000);

</script>
</body>
</html>
"""

# Отображаем игру на странице
components.html(game_html, height=620)