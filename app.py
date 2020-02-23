from flask import Flask
import torch
import boto3
from transformers import AlbertTokenizer, AlbertForQuestionAnswering

app = Flask(__name__)

def load_models():
    tokenizer = AlbertTokenizer.from_pretrained('./tokenizer_albert')
    model = AlbertForQuestionAnswering.from_pretrained('./model_data')
    return model, tokenizer

def question_answer(question, text):
    model, tokenizer = load_models()
    input_dict = tokenizer.encode_plus(question, text, return_tensors="pt")
    input_ids = input_dict["input_ids"].tolist()
    start_scores, end_scores = model(**input_dict)

    all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    answer = ''.join(all_tokens[torch.argmax(start_scores): torch.argmax(end_scores) + 1]).replace('▁', ' ').strip()
    return answer


@app.route('/')
def test_qa():
    question, text = "How many moods are there?", "My four moods: I'm too old for this shit! I'm too old for this shit! I'm too sober for this shit! I don't have time for this shit!"
    return(question_answer(question, text))

if __name__ == '__main__':
    app.run()