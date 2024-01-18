#!/usr/bin/env python3

from flask import Flask, render_template, request, session, redirect, url_for

from semantics import main, random_word_generator, provide_hint

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/", methods=["GET", "POST"])
def index():
    # Initialise session variables
    if "random_word" not in session and "synonyms" not in session:
        word_data = random_word_generator()
        session["random_word"] = word_data["random_word"]
        session["synonyms"] = word_data["synonyms"]

    if "synonyms" not in session:
        session["synonyms"] = []

    if "previous" not in session:
        session["previous"] = None

    if "previous_word" not in session:
        session["previous_word"] = None

    if "inputs" not in session:
        session["inputs"] = {}

    if "inputs_sort" not in session:
        session["inputs_sort"] = []

    if "inputs_sort_percent" not in session:
        session["inputs_sort_percent"] = {}

    if "current" not in session:
        session["current"] = 0.0

    random_word = session["random_word"]
    synonyms = session["synonyms"]
    previous = session["previous"]
    previous_word = session["previous_word"]
    inputs = session["inputs"]
    inputs_sort = session["inputs_sort"]
    inputs_sort_percent = session["inputs_sort_percent"]
    current = session["current"]

    #    random_word = "treasure"
    #    synonyms = ["money", "ship", "island", "riches", "pirates", "silver"]

    print(random_word)
    print(synonyms)

    restart = request.form.get("restart_game")
    if restart:
        [session.pop(key) for key in list(session.keys())]

    else:
        hint = None
        get_hints = request.form.get("get_hints")

        if request.method == "POST":
            print(request.form)

            if get_hints:
                if inputs_sort:
                    hints = provide_hint(
                        random_word, synonyms, max([inputs_sort[0][1], current])
                    )
                    inputs[previous_word] = previous
                    user_input, current = hints
                    previous = current
                    previous_word = user_input

                    inputs_sort = sorted(
                        inputs.items(), key=lambda x: float(x[1]), reverse=True
                    )
                    inputs_sort_percent = {
                        word: "{:.2%}".format(float(score))
                        for word, score in inputs_sort
                    }
                elif current:
                    inputs[previous_word] = previous
                    inputs_sort = sorted(
                        inputs.items(), key=lambda x: float(x[1]), reverse=True
                    )
                    inputs_sort_percent = {
                        word: "{:.2%}".format(float(score))
                        for word, score in inputs_sort
                    }
                    hints = provide_hint(random_word, synonyms, current)
                    user_input, current = hints
                    previous = current
                    previous_word = user_input

                else:
                    hints = provide_hint(random_word, synonyms, max([current, 0]))
                    user_input, current = hints
                    previous = current
                    previous_word = user_input

                current_percent = "{:.2%}".format(current)

            else:
                user_input = request.form["text_input"]

                if previous:
                    inputs[previous_word] = previous
                    current = main(user_input, random_word)[user_input]
                    previous = current
                    previous_word = user_input

                    inputs_sort = sorted(
                        inputs.items(), key=lambda x: float(x[1]), reverse=True
                    )
                    inputs_sort_percent = {
                        word: "{:.2%}".format(float(score))
                        for word, score in inputs_sort
                    }

                else:
                    current = main(user_input, random_word)[user_input]
                    previous = current
                    previous_word = user_input

            current_percent = "{:.2%}".format(current)

            session["previous"] = previous
            session["previous_word"] = previous_word
            session["inputs"] = inputs
            session["inputs_sort"] = inputs_sort
            session["inputs_sort_percent"] = inputs_sort_percent
            session["current"] = current

            return render_template(
                "index.html",
                current_percent=current_percent,
                input_word=user_input,
                inputs=inputs_sort_percent.items(),
                hint=hint,
            )
    return render_template("index.html")


@app.route("/give_up", methods=["POST"])
def give_up():
    print(request.form)
    if request.form.get("start_new") == "true":
        session.clear()
        return redirect(url_for("index"))
    else:
        return render_template("give_up.html", random_word=session["random_word"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
