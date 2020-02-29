from flask import Flask, render_template
from question_answer import question_answer

app = Flask(__name__)


@app.route('/qa')
def qa():
    question, text = "How many moods are there?", "My four moods: I'm too old for this shit! I'm too old for this shit! I'm too sober for this shit! I don't have time for this shit!"
    return(question_answer(question, text))


@app.route('/')
def base_page():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
