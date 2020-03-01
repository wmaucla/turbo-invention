from flask import Flask, render_template, request, jsonify
from question_answer import question_answer

app = Flask(__name__)


@app.route('/qa')
def qa():
    question, text = request.args.get("qaquestion"), request.args.get("qatext")
    print(question_answer(question, text))
    return jsonify({'html': question_answer(question, text)})


@app.route('/qa_page')
def qa_page():
    return render_template("qa.html")


@app.route('/')
def base_page():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
