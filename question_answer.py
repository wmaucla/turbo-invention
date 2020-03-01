import torch
import boto3
from transformers import AlbertTokenizer, AlbertForQuestionAnswering
import os


def load_models():
    # Download files locally if not exist from S3 bucket
    s3_bucket = boto3.resource('s3').Bucket('albert-model-files')
    for object in s3_bucket.objects.all():
        if object.key in ["config.json", "vocab.txt", "pytorch_model.bin"]:
            if not os.path.exists('model_data/{}'.format(object.key)):
                s3_bucket.download_file(object.key, 'model_data/{}'.format(object.key))

    for object in s3_bucket.objects.all():
        if object.key in ["special_tokens_map.json", "spiece.model", "tokenizer_config.json"]:
            if not os.path.exists('tokenizer_albert/{}'.format(object.key)):
                s3_bucket.download_file(object.key, 'tokenizer_albert/{}'.format(object.key))

    # Load pretrained models
    tokenizer = AlbertTokenizer.from_pretrained('./tokenizer_albert')
    model = AlbertForQuestionAnswering.from_pretrained('./model_data')
    return model, tokenizer


def question_answer(question, text):
    # Torch code to return output from pretrained models
    model, tokenizer = load_models()
    input_dict = tokenizer.encode_plus(question, text, return_tensors="pt")
    input_ids = input_dict["input_ids"].tolist()
    start_scores, end_scores = model(**input_dict)
    all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    answer = ''.join(all_tokens[torch.argmax(start_scores): torch.argmax(end_scores) + 1]).replace('▁', ' ').strip()
    return answer