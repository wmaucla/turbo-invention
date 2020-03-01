from flask import Flask, render_template, request, jsonify
from question_answer import question_answer

app = Flask(__name__)


@app.route('/qa')
def qa():
    question, text = request.args.get("qaquestion"), request.args.get("qatext")
    return jsonify({'html': question_answer(question, text)})


@app.route('/qa_static', methods=['POST'])
def qa_static():
    question, text = request.form["qaquestion"], request.form["qatext"]
    return render_template("qa_static.html", response=question_answer(question, text), text=text, question=question)


@app.route('/qa_page')
def qa_page():
    return render_template("qa.html")


@app.route('/')
@app.route('/home')
def base_page():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
