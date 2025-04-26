from flask import Flask, render_template, request, jsonify, session
import os
import json
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Game data with 10 levels
levels = [
    # Level 1: Basic introduction
    {
        "name": "Level 1: Network Foundations",
        "platforms": [
            {"x": 0, "y": 450, "width": 200, "height": 30},  # Spawn platform
            {"x": 250, "y": 400, "width": 200, "height": 30},
            {"x": 500, "y": 350, "width": 200, "height": 30},
            {"x": 650, "y": 300, "width": 150, "height": 30}  # Platform near endpoint
        ],
        "collectibles": [
            {"x": 100, "y": 420},
            {"x": 350, "y": 370},
            {"x": 600, "y": 320}
        ],
        "enemies": [
            {"x": 300, "y": 370, "type": "bug", "movement": "horizontal", "range": 100}
        ],
        "endpoint": {"x": 700, "y": 270}  # Moved closer to last platform
    },
    
    # Level 2: Zigzag pattern
    {
        "name": "Level 2: Data Pathways",
        "platforms": [
            {"x": 0, "y": 450, "width": 150, "height": 30},  # Spawn platform
            {"x": 200, "y": 400, "width": 150, "height": 30},
            {"x": 0, "y": 350, "width": 150, "height": 30},
            {"x": 200, "y": 300, "width": 150, "height": 30},
            {"x": 0, "y": 250, "width": 150, "height": 30},
            {"x": 200, "y": 200, "width": 150, "height": 30},
            {"x": 600, "y": 150, "width": 200, "height": 30}  # Platform near endpoint
        ],
        "collectibles": [
            {"x": 75, "y": 420},
            {"x": 275, "y": 370},
            {"x": 75, "y": 320},
            {"x": 275, "y": 270}
        ],
        "enemies": [
            {"x": 100, "y": 370, "type": "virus", "movement": "vertical", "range": 50}
        ],
        "endpoint": {"x": 700, "y": 120}  # Moved closer to last platform
    },

    # Level 3: Staircase pattern
    {
        "name": "Level 3: Protocol Steps",
        "platforms": [
            {"x": 0, "y": 450, "width": 100, "height": 30},  # Spawn platform
            {"x": 150, "y": 400, "width": 100, "height": 30},
            {"x": 300, "y": 350, "width": 100, "height": 30},
            {"x": 450, "y": 300, "width": 100, "height": 30},
            {"x": 600, "y": 250, "width": 150, "height": 30}  # Extended platform near endpoint
        ],
        "collectibles": [
            {"x": 50, "y": 420},
            {"x": 200, "y": 370},
            {"x": 350, "y": 320},
            {"x": 500, "y": 270}
        ],
        "enemies": [
            {"x": 200, "y": 370, "type": "trojan", "movement": "horizontal", "range": 150}
        ],
        "endpoint": {"x": 650, "y": 220}  # Moved closer to last platform
    },

    # Level 4: Pyramid pattern
    {
        "name": "Level 4: Security Layers",
        "platforms": [
            {"x": 0, "y": 450, "width": 100, "height": 30},  # Added spawn platform
            {"x": 350, "y": 450, "width": 100, "height": 30},
            {"x": 300, "y": 400, "width": 200, "height": 30},
            {"x": 250, "y": 350, "width": 300, "height": 30},
            {"x": 200, "y": 300, "width": 400, "height": 30},
            {"x": 600, "y": 250, "width": 200, "height": 30}  # Platform near endpoint
        ],
        "collectibles": [
            {"x": 400, "y": 420},
            {"x": 400, "y": 370},
            {"x": 400, "y": 320},
            {"x": 400, "y": 270}
        ],
        "enemies": [
            {"x": 300, "y": 370, "type": "worm", "movement": "horizontal", "range": 200},
            {"x": 400, "y": 320, "type": "virus", "movement": "vertical", "range": 50}
        ],
        "endpoint": {"x": 700, "y": 220}  # Moved closer to last platform
    },

    # Level 5: Floating islands
    {
        "name": "Level 5: Cloud Nodes",
        "platforms": [
            {"x": 0, "y": 450, "width": 100, "height": 30},  # Added spawn platform
            {"x": 50, "y": 450, "width": 100, "height": 30},
            {"x": 300, "y": 400, "width": 100, "height": 30},
            {"x": 150, "y": 350, "width": 100, "height": 30},
            {"x": 400, "y": 300, "width": 100, "height": 30},
            {"x": 250, "y": 250, "width": 100, "height": 30},
            {"x": 500, "y": 200, "width": 200, "height": 30}  # Extended platform near endpoint
        ],
        "collectibles": [
            {"x": 100, "y": 420},
            {"x": 350, "y": 370},
            {"x": 200, "y": 320},
            {"x": 450, "y": 270},
            {"x": 300, "y": 220}
        ],
        "enemies": [
            {"x": 350, "y": 370, "type": "malware", "movement": "circular", "radius": 50},
            {"x": 450, "y": 270, "type": "bug", "movement": "horizontal", "range": 100}
        ],
        "endpoint": {"x": 600, "y": 170}  # Moved closer to last platform
    },

    # Level 6: Maze-like structure
    {
        "name": "Level 6: Network Maze",
        "platforms": [
            {"x": 0, "y": 450, "width": 100, "height": 30},  # Spawn platform
            {"x": 0, "y": 450, "width": 300, "height": 30},
            {"x": 400, "y": 450, "width": 400, "height": 30},
            {"x": 0, "y": 350, "width": 200, "height": 30},
            {"x": 300, "y": 350, "width": 200, "height": 30},
            {"x": 600, "y": 350, "width": 200, "height": 30},
            {"x": 100, "y": 250, "width": 300, "height": 30},
            {"x": 500, "y": 250, "width": 300, "height": 30},
            {"x": 700, "y": 200, "width": 100, "height": 30}  # Platform near endpoint
        ],
        "collectibles": [
            {"x": 150, "y": 420},
            {"x": 450, "y": 420},
            {"x": 100, "y": 320},
            {"x": 400, "y": 320},
            {"x": 700, "y": 320},
            {"x": 250, "y": 220},
            {"x": 550, "y": 220}
        ],
        "enemies": [
            {"x": 200, "y": 420, "type": "virus", "movement": "horizontal", "range": 200},
            {"x": 500, "y": 420, "type": "trojan", "movement": "horizontal", "range": 200},
            {"x": 350, "y": 320, "type": "worm", "movement": "vertical", "range": 50}
        ],
        "endpoint": {"x": 750, "y": 170}  # Moved closer to last platform
    },

    # Level 7: Vertical challenge
    {
        "name": "Level 7: Firewall Ascent",
        "platforms": [
            {"x": 0, "y": 450, "width": 100, "height": 30},  # Spawn platform
            {"x": 200, "y": 400, "width": 100, "height": 30},
            {"x": 0, "y": 350, "width": 100, "height": 30},
            {"x": 200, "y": 300, "width": 100, "height": 30},
            {"x": 0, "y": 250, "width": 100, "height": 30},
            {"x": 200, "y": 200, "width": 100, "height": 30},
            {"x": 0, "y": 150, "width": 100, "height": 30},
            {"x": 200, "y": 100, "width": 200, "height": 30}  # Platform near endpoint
        ],
        "collectibles": [
            {"x": 50, "y": 420},
            {"x": 250, "y": 370},
            {"x": 50, "y": 320},
            {"x": 250, "y": 270},
            {"x": 50, "y": 220},
            {"x": 250, "y": 170}
        ],
        "enemies": [
            {"x": 150, "y": 370, "type": "bug", "movement": "horizontal", "range": 300, "speed": 3},
            {"x": 150, "y": 270, "type": "virus", "movement": "horizontal", "range": 300, "speed": 3}
        ],
        "endpoint": {"x": 300, "y": 100}  # Moved closer to last platform
    },

    # Level 8: Narrow platforms
    {
        "name": "Level 8: Bandwidth Challenge",
        "platforms": [
            {"x": 0, "y": 450, "width": 100, "height": 20},  # Wider spawn platform
            {"x": 100, "y": 400, "width": 50, "height": 20},
            {"x": 200, "y": 350, "width": 50, "height": 20},
            {"x": 300, "y": 300, "width": 50, "height": 20},
            {"x": 400, "y": 250, "width": 50, "height": 20},
            {"x": 500, "y": 200, "width": 50, "height": 20},
            {"x": 600, "y": 150, "width": 100, "height": 20},  # Wider platform near endpoint
            {"x": 700, "y": 100, "width": 100, "height": 30}   # Final platform
        ],
        "collectibles": [
            {"x": 50, "y": 430},
            {"x": 125, "y": 380},
            {"x": 225, "y": 330},
            {"x": 325, "y": 280},
            {"x": 425, "y": 230},
            {"x": 525, "y": 180}
        ],
        "enemies": [
            {"x": 150, "y": 380, "type": "worm", "movement": "vertical", "range": 100},
            {"x": 350, "y": 280, "type": "malware", "movement": "vertical", "range": 100}
        ],
        "endpoint": {"x": 750, "y": 70}  # Moved closer to last platform
    },

    # Level 9: Moving platforms
    {
        "name": "Level 9: Packet Routing",
        "platforms": [
            {"x": 0, "y": 450, "width": 150, "height": 30},  # Wider spawn platform
            {"x": 200, "y": 400, "width": 100, "height": 30, "movement": "horizontal", "range": 200, "speed": 2},
            {"x": 400, "y": 350, "width": 100, "height": 30, "movement": "vertical", "range": 100, "speed": 1.5},
            {"x": 600, "y": 300, "width": 150, "height": 30, "movement": "horizontal", "range": 150, "speed": 3},
            {"x": 700, "y": 250, "width": 100, "height": 30}  # Stationary platform near endpoint
        ],
        "collectibles": [
            {"x": 75, "y": 420},
            {"x": 250, "y": 370},
            {"x": 450, "y": 320},
            {"x": 650, "y": 270}
        ],
        "enemies": [
            {"x": 300, "y": 370, "type": "virus", "movement": "horizontal", "range": 200},
            {"x": 500, "y": 320, "type": "trojan", "movement": "vertical", "range": 100}
        ],
        "endpoint": {"x": 750, "y": 220}  # Moved closer to last platform
    },

    # Level 10: Final challenge
    {
        "name": "Level 10: System Mastery",
        "platforms": [
            {"x": 0, "y": 450, "width": 150, "height": 30},  # Wider spawn platform
            {"x": 150, "y": 420, "width": 100, "height": 30},
            {"x": 300, "y": 390, "width": 100, "height": 30},
            {"x": 450, "y": 360, "width": 100, "height": 30},
            {"x": 600, "y": 330, "width": 150, "height": 30},
            {"x": 100, "y": 300, "width": 100, "height": 30},
            {"x": 250, "y": 270, "width": 100, "height": 30},
            {"x": 400, "y": 240, "width": 100, "height": 30},
            {"x": 550, "y": 210, "width": 100, "height": 30},
            {"x": 700, "y": 180, "width": 150, "height": 30}  # Extended final platform
        ],
        "collectibles": [
            {"x": 75, "y": 420},
            {"x": 150, "y": 270},
            {"x": 450, "y": 210},
            {"x": 600, "y": 180}
        ],
        "enemies": [
            {"x": 200, "y": 390, "type": "virus", "movement": "circular", "radius": 50, "speed": 2},
            {"x": 350, "y": 360, "type": "trojan", "movement": "circular", "radius": 50, "speed": 2},
            {"x": 500, "y": 330, "type": "worm", "movement": "circular", "radius": 50, "speed": 2},
            {"x": 300, "y": 240, "type": "malware", "movement": "circular", "radius": 50, "speed": 2}
        ],
        "endpoint": {"x": 750, "y": 150},
        "victory_song": "rickroll.mp3"  # Changed to rickroll.mp3
    }
]

@app.route('/')
def index():
    session['score'] = 0
    session['level'] = 0
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/api/level', methods=['GET'])
def get_level():
    level_id = request.args.get('level', '0')
    try:
        level_id = int(level_id)
        if 0 <= level_id < len(levels):
            return jsonify(levels[level_id])
        else:
            return jsonify({"error": "Level not found"}), 404
    except ValueError:
        return jsonify({"error": "Invalid level ID"}), 400

if __name__ == '__main__':
    app.run(debug=True)