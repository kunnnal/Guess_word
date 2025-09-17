from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Word list
WORDS = ["code", "java", "data", "play", "game", "ball", "cat", "dog", "run", "book"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_word")
def get_word():
    word = random.choice(WORDS)
    return jsonify({"word": word})

@app.route("/check_guess", methods=["POST"])
def check_guess():
    data = request.json
    guess = data.get("guess", "").lower()
    word = data.get("word", "").lower()

    if guess == word:
        return jsonify({"result": "✅ Correct!", "game_over": True})
    else:
        matches = sum(1 for g, w in zip(guess, word) if g == w)
        return jsonify({"result": f"❌ Wrong. {matches} letters in the right place.", "game_over": False})

if __name__ == "__main__":
    app.run(debug=True)
