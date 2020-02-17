from flask import Flask, render_template, url_for, redirect
app = Flask(__name__)
from question_answer import from_question_return_answer

@app.route('/')
def base_page():
    return render_template("index.html")

@app.route('/qa')
def get_question_answer():
    question, text = "How many moods are there?", "My four moods: I'm too old for this shit! I'm too old for this shit! I'm too sober for this shit! I don't have time for this shit!"
    return from_question_return_answer(question, text)

if __name__ == '__main__':
    app.run(debug=True)