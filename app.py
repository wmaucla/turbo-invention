from flask import Flask
from transformers import *
import torch
import boto3

app = Flask(__name__)

def load_models():
    bucketname = 'qaexample'  # replace with your bucket name
    s3 = boto3.resource('s3').Bucket(bucketname)
    for object in s3.objects.all():
        if object.key in ["special_tokens_map.json", "tokenizer_config.json", "vocab.txt"]:
            s3.download_file(object.key, 'tokenizer_s3/{}'.format(object.key))
        elif object.key in ["config.json", "pytorch_model.bin"]:
            s3.download_file(object.key, 'model_data/{}'.format(object.key))

    tokenizer = BertTokenizer.from_pretrained('./tokenizer_s3')
    model = BertForQuestionAnswering.from_pretrained('./model_data')
    return model, tokenizer

def question_answer(question, text):
    model, tokenizer = load_models()
    input_text = "[CLS]" + question + " [SEP] " + text + " [SEP]"
    input_ids = tokenizer.encode(input_text)
    token_type_ids = [0 if i <= input_ids.index(102) else 1 for i in range(len(input_ids))]
    start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))
    all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    return (' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores) +1]))


@app.route('/bleh')
def meh():
    return "Welcome, master ma.", 200

@app.route('/')
def test_qa():
    question, text = "How many moods are there?", "My four moods: I'm too old for this shit! I'm too old for this shit! I'm too sober for this shit! I don't have time for this shit!"
    return(question_answer(question, text))

if __name__ == '__main__':
    app.run()