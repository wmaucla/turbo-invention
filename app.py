from flask import Flask
app = Flask(__name__)
from question_answer import *

@app.route('/bleh')
def meh():
    return "Welcome, master ma.", 200

@app.route('/')
def test_qa():
    question, text = "How many moods are there?", "My four moods: I'm too old for this shit! I'm too old for this shit! I'm too sober for this shit! I don't have time for this shit!"
    return(question_answer(question, text))

if __name__ == '__main__':
    app.run()