from transformers import *
import torch
import boto3
import pickle

def question_answer(question, text, model, tokenizer):
    input_text = "[CLS]" + question + " [SEP] " + text + " [SEP]"
    input_ids = tokenizer.encode(input_text)
    token_type_ids = [0 if i <= input_ids.index(102) else 1 for i in range(len(input_ids))]
    start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))
    all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    return (' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores) +1]))


"""
if __name__ == "__main__":
    tokenizer = BertTokenizer.from_pretrained('./tokenizer_s3')
    model = BertForQuestionAnswering.from_pretrained('./model_data')
    print(question_answer("Who is John?", "I eat pizza. John is a criminal", model, tokenizer))
    bucketname = 'qaexample'  # replace with your bucket name
    s3 = boto3.resource('s3').Bucket(bucketname)
    # s3.Bucket(bucketname).download_file("special_tokens_map.json", 'tokenizer_s3/coasdfaig1.json')

        for object in s3.objects.all():
        if object.key in ["special_tokens_map.json", "tokenizer_config.json", "vocab.txt"]:
            s3.download_file(object.key, 'tokenizer_s3/{}'.format(object.key))
        elif object.key in ["config.json", "pytorch_model.bin"]:
            s3.download_file(object.key, 'model_data/{}'.format(object.key))
"""

if __name__ == "__main__":
    # model = AutoModel.from_pretrained("distilbert-base-multilingual-cased")

    # model = BertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
    # model.save_pretrained("/home/william/Documents/repos/turbo-invention/model_data/")

    from transformers import AlbertTokenizer, AlbertForQuestionAnswering
    import torch

    tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')
    model = AlbertForQuestionAnswering.from_pretrained('./model_data')

    question, text = "How many moods are there?", "My four moods: I'm too old for this shit! I'm too cold for this shit! I'm too sober for this shit! I don't have time for this shit!"

    input_dict = tokenizer.encode_plus(question, text, return_tensors="pt")
    input_ids = input_dict["input_ids"].tolist()
    start_scores, end_scores = model(**input_dict)

    all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    answer = ''.join(all_tokens[torch.argmax(start_scores): torch.argmax(end_scores) + 1]).replace('▁', ' ').strip()
    print(answer)