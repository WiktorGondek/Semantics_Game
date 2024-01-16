#!/usr/bin/env python3

from flask import Flask, render_template, request

from semantics import main, random_word_generator, provide_hint

app = Flask(__name__)

# random_word = random_word_generator()["random_word"]
inputs = {}
random_word = "treasure"
previous = None
previous_word = None


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        global previous, previous_word
        user_input = request.form["text_input"]

        if previous:
            inputs[previous_word] = previous
            current = main(user_input, random_word)[user_input]
            previous = current
            previous_word = user_input
        else:
            current = main(user_input, random_word)[user_input]
            previous = current
            previous_word = user_input

        inputs_sort = sorted(inputs.items(), key=lambda x: float(x[1]), reverse=True)
        print(inputs_sort)
        inputs_sort_percent = {
            word: "{:.2%}".format(float(score)) for word, score in inputs_sort
        }
        print(inputs_sort_percent)
        current_percent = "{:.2%}".format(current)

        synonyms = ["money", "ship", "island", "riches", "pirates", "silver"]
        # if len(inputs_sort) > 1:
        #    hint = provide_hint(
        #        random_word, synonyms, float(inputs_sort[0][1].replace("%", ""))
        #    )
        # else:
        #    hint = "No hints available"
        # try:
        #    hint = provide_hint(synonyms, inputs_sort[0][1].replace("%", ""))
        # except:
        #    hint = "No hints available"
        # print(hint)

        return render_template(
            "index.html",
            input_word=user_input,
            current=current_percent,
            inputs=inputs_sort_percent.items(),
        )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
