const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

canvas.width = 800;
canvas.height = 500;

// Load all game images
const images = {
    background: loadImage('/static/img/tech-background.png'),
    player: loadImage('/static/img/player.png'),
    bug: loadImage('/static/img/bug.png'),
    virus: loadImage('/static/img/virus.png'),
    malware: loadImage('/static/img/malware.png'),
    codeSnippet: loadImage('/static/img/code-snippet.png'),
    server: loadImage('/static/img/server.png')
};

function loadImage(src) {
    const img = new Image();
    img.src = src;
    return img;
}

// Game State
let gameState = {
    player: {
        x: 50,
        y: 400,
        width: 40,
        height: 50,
        velocityX: 0,
        velocityY: 0,
        grounded: false,
        speed: 5,
        jumpPower: 15,
        lives: 3
    },
    keys: {},
    platforms: [],
    collectibles: [],
    enemies: [],
    endpoint: {},
    score: 0,
    currentLevel: 0,
    levelComplete: false,
    gameOver: false
};

// Listen for key inputs
document.addEventListener('keydown', (e) => {
    gameState.keys[e.key] = true;
});
document.addEventListener('keyup', (e) => {
    gameState.keys[e.key] = false;
});

// Load level data from Flask
async function loadLevel(levelId) {
    try {
        const res = await fetch(`/api/level?level=${levelId}`);
        const level = await res.json();

        document.getElementById('level-name').textContent = level.name || "Unknown Level";

        gameState.platforms = level.platforms || [];
        gameState.collectibles = (level.collectibles || []).map(c => ({ ...c, collected: false }));
        gameState.enemies = level.enemies || [];
        gameState.endpoint = level.endpoint || {};

        gameState.enemies.forEach(enemy => {
            if (enemy.movement === 'horizontal') enemy.startX = enemy.x;
            if (enemy.movement === 'vertical') enemy.startY = enemy.y;
            enemy.direction = 1;
        });

        resetPlayerPosition();
        if (!gameLoopRunning) {
            gameLoop();
            gameLoopRunning = true;
        }
    } catch (error) {
        console.error('Error loading level:', error);
        alert('Failed to load level.');
    }
}

let gameLoopRunning = false;

// Game Loop
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.drawImage(images.background, 0, 0, canvas.width, canvas.height);

    updatePlayer();
    updateEnemies();
    checkCollisions();
    drawGameElements();

    if (checkLevelComplete() && !gameState.levelComplete) {
        gameState.levelComplete = true;
        if (gameState.currentLevel < 19) {
            showMessage('Level Complete!', 'You collected all code snippets and reached the server!', true);
        } else {
            showMessage('Congratulations!', 'You completed the final level!', false);
        }
    }

    if (gameState.player.lives <= 0 && !gameState.gameOver) {
        gameState.gameOver = true;
        showMessage('Game Over', 'You ran out of lives! Try again?', false);
    }

    if (!gameState.gameOver || gameState.levelComplete) {
        requestAnimationFrame(gameLoop);
    }
}

function updatePlayer() {
    gameState.player.velocityY += 0.8; // Gravity
    gameState.player.grounded = false;

    gameState.platforms.forEach(platform => {
        if (gameState.player.y + gameState.player.height <= platform.y &&
            gameState.player.y + gameState.player.height + gameState.player.velocityY >= platform.y &&
            gameState.player.x + gameState.player.width > platform.x &&
            gameState.player.x < platform.x + platform.width) {
            gameState.player.grounded = true;
            gameState.player.velocityY = 0;
            gameState.player.jumping = false;
            gameState.player.y = platform.y - gameState.player.height;
        }
    });

    if ((gameState.keys['ArrowLeft'] || gameState.keys['a']) && !gameState.levelComplete) {
        gameState.player.velocityX = -gameState.player.speed;
    } else if ((gameState.keys['ArrowRight'] || gameState.keys['d']) && !gameState.levelComplete) {
        gameState.player.velocityX = gameState.player.speed;
    } else {
        gameState.player.velocityX = 0;
    }

    if ((gameState.keys['ArrowUp'] || gameState.keys['w'] || gameState.keys[' ']) &&
        gameState.player.grounded && !gameState.levelComplete) {
        gameState.player.jumping = true;
        gameState.player.velocityY = -gameState.player.jumpPower;
    }

    gameState.player.x += gameState.player.velocityX;
    gameState.player.y += gameState.player.velocityY;

    if (gameState.player.x < 0) gameState.player.x = 0;
    if (gameState.player.x + gameState.player.width > canvas.width) gameState.player.x = canvas.width - gameState.player.width;
    if (gameState.player.y > canvas.height) {
        gameState.player.lives--;
        document.getElementById('lives').textContent = gameState.player.lives;
        resetPlayerPosition();
    }
}

function updateEnemies() {
    gameState.enemies.forEach(enemy => {
        if (enemy.movement === 'horizontal') {
            enemy.x += enemy.direction * 2;
            if (Math.abs(enemy.x - enemy.startX) > enemy.range) {
                enemy.direction *= -1;
            }
        }
        if (enemy.movement === 'vertical') {
            enemy.y += enemy.direction * 1.5;
            if (Math.abs(enemy.y - enemy.startY) > enemy.range) {
                enemy.direction *= -1;
            }
        }
    });
}

function checkCollisions() {
    gameState.collectibles.forEach(collectible => {
        if (!collectible.collected &&
            gameState.player.x < collectible.x + 30 &&
            gameState.player.x + gameState.player.width > collectible.x &&
            gameState.player.y < collectible.y + 30 &&
            gameState.player.y + gameState.player.height > collectible.y) {
            collectible.collected = true;
            gameState.score += 100;
            document.getElementById('score').textContent = gameState.score;
        }
    });

    gameState.enemies.forEach(enemy => {
        if (gameState.player.x < enemy.x + 40 &&
            gameState.player.x + gameState.player.width > enemy.x &&
            gameState.player.y < enemy.y + 40 &&
            gameState.player.y + gameState.player.height > enemy.y) {
            gameState.player.lives--;
            document.getElementById('lives').textContent = gameState.player.lives;
            resetPlayerPosition();
        }
    });
}

function drawGameElements() {
    // Draw platforms
    ctx.fillStyle = '#5bffbc';
    gameState.platforms.forEach(p => {
        ctx.fillRect(p.x, p.y, p.width, p.height);
    });

    // Draw collectibles
    gameState.collectibles.forEach(c => {
        if (!c.collected) {
            ctx.drawImage(images.codeSnippet, c.x, c.y, 30, 30);
        }
    });

    // Draw enemies
    gameState.enemies.forEach(e => {
        let img = images.bug;
        if (e.type === 'virus') img = images.virus;
        if (e.type === 'malware') img = images.malware;
        ctx.drawImage(img, e.x, e.y, 40, 40);
    });

    // Draw endpoint
    ctx.drawImage(images.server, gameState.endpoint.x, gameState.endpoint.y, 50, 50);

    // Draw player
    ctx.drawImage(images.player, gameState.player.x, gameState.player.y, gameState.player.width, gameState.player.height);
}

function resetPlayerPosition() {
    gameState.player.x = 50;
    gameState.player.y = 400;
    gameState.player.velocityX = 0;
    gameState.player.velocityY = 0;
}

function checkLevelComplete() {
    const allCollected = gameState.collectibles.every(c => c.collected);
    const atEndpoint = gameState.player.x < gameState.endpoint.x + 50 &&
                        gameState.player.x + gameState.player.width > gameState.endpoint.x &&
                        gameState.player.y < gameState.endpoint.y + 50 &&
                        gameState.player.y + gameState.player.height > gameState.endpoint.y;
    return allCollected && atEndpoint;
}

function showMessage(title, text, showNext) {
    document.getElementById('message-title').textContent = title;
    document.getElementById('message-text').textContent = text;
    document.getElementById('next-level-btn').style.display = showNext ? 'inline-block' : 'none';
    document.getElementById('message-box').classList.remove('hidden');
}

function loadNextLevel() {
    document.getElementById('message-box').classList.add('hidden');
    if (gameState.currentLevel < 19) {
        gameState.currentLevel++;
        gameState.levelComplete = false;
        gameLoopRunning = false;
        loadLevel(gameState.currentLevel);
    }
}

// Button listeners
document.getElementById('next-level-btn').addEventListener('click', loadNextLevel);
document.getElementById('restart-btn').addEventListener('click', () => {
    document.getElementById('message-box').classList.add('hidden');
    if (gameState.gameOver) {
        gameState.player.lives = 3;
        gameState.score = 0;
        document.getElementById('score').textContent = 0;
        document.getElementById('lives').textContent = 3;
        gameState.gameOver = false;
    }
    gameState.levelComplete = false;
    gameLoopRunning = false;
    loadLevel(gameState.currentLevel);
});

// Wait for all images to load before starting
window.addEventListener('load', () => {
    console.log('Window loaded');
    loadLevel(0);
});
