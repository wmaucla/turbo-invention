from flask import Flask
from question_answer import question_answer


app = Flask(__name__)


@app.route('/')
def qa():
    question, text = "How many moods are there?", "My four moods: I'm too old for this shit! I'm too old for this shit! I'm too sober for this shit! I don't have time for this shit!"
    return(question_answer(question, text))


if __name__ == "__main__":
    print(qa())