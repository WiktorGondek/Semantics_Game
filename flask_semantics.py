#!/usr/bin/env python3

import argparse

from flask import Flask, redirect, render_template, request, session, url_for

from semantics import main, provide_hint, random_word_generator

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/", methods=["GET", "POST"])
def main_page():
    """Main page to handle text input"""
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

    print(synonyms)

    # Clear session variables when restart button pressed
    restart = request.form.get("restart_game")
    if restart:
        [session.pop(key) for key in list(session.keys())]

    else:
        get_hints = request.form.get("get_hints")

        if request.method == "POST":
            print(request.form)

            # Handle case where get hint button is pressed
            if get_hints:
                inputs[previous_word] = previous
                if inputs_sort:
                    current = (
                        max(inputs_sort[0][1], current)
                        if inputs_sort[0][1] is not None
                        else current
                    )

                # Determine the next hint from synonyms
                hints = provide_hint(random_word, synonyms, current)
                user_input, current = hints
                previous = current
                previous_word = user_input

                # Sort the inputs dictionary
                inputs_sort = sorted(
                    inputs.items(),
                    key=lambda x: float("-inf") if x[1] is None else x[1],
                    reverse=True,
                )

                # Return percentage values in inputs_sort
                inputs_sort_percent = {
                    word: "{:.2%}".format(score)
                    for word, score in inputs_sort
                    if score is not None
                }

                # Return percentage value for current word
                current_percent = "{:.2%}".format(current)

            # Handle case where text is input into text box
            else:
                user_input = request.form["text_input"]

                # Handle case where previous word exists
                if previous:
                    inputs[previous_word] = previous
                    current = main(random_word, user_input)[user_input]
                    previous = current

                    inputs_sort = sorted(
                        inputs.items(),
                        key=lambda x: float("-inf") if x[1] is None else x[1],
                        reverse=True,
                    )
                    inputs_sort_percent = {
                        word: "{:.2%}".format(score)
                        for word, score in inputs_sort
                        if score is not None
                    }
                    previous_word = user_input

                # Handle case where no previous word exists
                else:
                    current = main(random_word, user_input)[user_input]
                    previous = current
                    previous_word = user_input

            current_percent = "{:.2%}".format(current)

            # Assign session variables
            session["previous"] = previous
            session["previous_word"] = previous_word
            session["inputs"] = inputs
            session["inputs_sort"] = inputs_sort
            session["inputs_sort_percent"] = inputs_sort_percent
            session["current"] = current

            return render_template(
                "main_page.html",
                current_percent=current_percent,
                input_word=user_input,
                inputs=inputs_sort_percent.items(),
            )
    return render_template("main_page.html")


@app.route("/give_up", methods=["POST"])
def give_up():
    """Page to handle the case when give up button is pressed"""

    if "random_word" in session:
        # Handle case when start new button is pressed
        if request.form.get("start_new") == "true":
            session.clear()
            return redirect(url_for("main_page"))
        # Return the give_up.html template
        else:
            return render_template("give_up.html", random_word=session["random_word"])
    # Redirect to main page if no random_word exists
    else:
        return redirect(url_for("main_page"))


def create_app():
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    print(args)

    app.run(host="0.0.0.0", port=8000, **vars(args))
