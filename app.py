from flask import Flask, render_template, request, jsonify
from question_answer import question_answer

app = Flask(__name__)


@app.route('/qa', methods=['GET', 'POST'])
def qa():
    print(request.args)
    question, text = request.args.get("qa_question"), request.args.get("qa_text")
    print(question, text)
    return jsonify({'qa_response': question_answer(question, text)})


@app.route('/qa_page')
def qa_page():
    return render_template("qa.html")


@app.route('/')
def base_page():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
