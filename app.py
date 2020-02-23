from flask import Flask
import torch
import boto3
from transformers import AlbertTokenizer, AlbertForQuestionAnswering
import pickle
from io import BytesIO

app = Flask(__name__)

def load_models():
    """s3_bucket = boto3.resource('s3').Bucket('albert-model-files')
    for object in s3_bucket.objects.all():
        if object.key in ["config.json", "vocab.txt"]:
            s3_bucket.download_file(object.key, 'model_data/{}'.format(object.key))

    s3 = boto3.resource('s3')
    obj = s3.Object('albert-model-files', 'pytorch_model.bin')"""
    # body = obj.get()['Body'].read()


    tokenizer = AlbertTokenizer.from_pretrained('./tokenizer_albert')
    # model = AlbertForQuestionAnswering.from_pretrained('./model_data')
    model = AlbertForQuestionAnswering.from_pretrained('albert-base-v1')
    import pdb
    pdb.set_trace()
    return model, tokenizer

def question_answer(question, text):
    model, tokenizer = load_models()

    import pdb
    pdb.set_trace()
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
    test_qa()