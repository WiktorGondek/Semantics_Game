#!/usr/bin/env python3

from flask import Flask, render_template, request

from semantics import main, random_word_generator

app = Flask(__name__)

random_word = random_word_generator()["random_word"]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["text_input"]
        sem = main(user_input, "untidy")
        return render_template("index.html", sem=sem)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
