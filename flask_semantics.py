#!/usr/bin/env python3

from flask import Flask, render_template, request

from semantics import main, random_word_generator, provide_hint

app = Flask(__name__)

# random_word = random_word_generator()["random_word"]
inputs = {}
random_word = "treasure"
previous = None
previous_word = None
synonyms = ["money", "ship", "island", "riches", "pirates", "silver"]


@app.route("/", methods=["GET", "POST"])
def index():
    global inputs_sort
    hint = None
    get_hints = request.form.get("get_hints")

    if request.method == "POST":
        print(request.form)
        global previous, previous_word

        if get_hints:
            hints = provide_hint(random_word, synonyms, inputs_sort[0][1])
            if hints:
                inputs[previous_word] = previous
                user_input, current = hints
                previous = current
                previous_word = user_input
            else:
                user_input, current = "", 0.0

            inputs_sort = sorted(
                inputs.items(), key=lambda x: float(x[1]), reverse=True
            )
            inputs_sort_percent = {
                word: "{:.2%}".format(float(score)) for word, score in inputs_sort
            }
            current_percent = "{:.2%}".format(current)

        else:
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
        inputs_sort_percent = {
            word: "{:.2%}".format(float(score)) for word, score in inputs_sort
        }
        current_percent = "{:.2%}".format(current)

        #    if inputs_sort:
        #        hint = provide_hint(random_word, synonyms, inputs_sort[0][1])
        # print(inputs_sort[0][1])
        # print(hint)
        # print(inputs_sort_percent.items())

        # if len(inputs_sort) > 1:
        #    hint = provide_hint(
        #        random_word, synonyms, float(inputs_sort[0][1].replace("%", ""))
        #    )
        # else:
        #    hint = "no hints available"
        # try:
        #    hint = provide_hint(synonyms, inputs_sort[0][1].replace("%", ""))
        # except:
        #    hint = "no hints available"
        # print(hint)
        # iif get_hints:
        #    print("bogos binted")
        # hints = provide_hints(random_word, synonyms, inputs)
        # for word in hints:
        #    inputs[word] = hints[word]

        return render_template(
            "index.html",
            current_percent=current_percent,
            input_word=user_input,
            inputs=inputs_sort_percent.items(),
            hint=hint,
        )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
