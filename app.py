from flask import Flask, jsonify, render_template, request, session
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "guess-word-dev-secret"

# Word list
WORDS = ["code", "java", "data", "play", "game", "ball", "cat", "dog", "run", "book"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_word")
def get_word():
    word = random.choice(WORDS)
    session["word"] = word
    return jsonify({"length": len(word)})


@app.route("/check_guess", methods=["POST"])
def check_guess():
    data = request.get_json(silent=True) or {}
    guess = data.get("guess", "").strip().lower()
    word = session.get("word")

    if not word:
        return (
            jsonify(
                {
                    "result": "Start a new game first.",
                    "game_over": True,
                    "error": "missing_word",
                }
            ),
            400,
        )

    if not guess:
        return (
            jsonify(
                {
                    "result": "Please enter a guess.",
                    "game_over": False,
                    "error": "missing_guess",
                }
            ),
            400,
        )

    if len(guess) != len(word):
        return (
            jsonify(
                {
                    "result": f"Guess must be {len(word)} letters long.",
                    "game_over": False,
                    "error": "invalid_length",
                }
            ),
            400,
        )

    if guess == word:
        session.pop("word", None)
        return jsonify({"result": "✅ Correct!", "game_over": True})

    matches = sum(1 for g, w in zip(guess, word) if g == w)
    return jsonify(
        {
            "result": f"❌ Wrong. {matches} letters in the right place.",
            "game_over": False,
        }
    )


if __name__ == "__main__":
    app.run()
