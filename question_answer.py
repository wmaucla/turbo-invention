"""
from transformers import *
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')


def from_question_return_answer(question, text):
    input_text = "[CLS]" + question + " [SEP] " + text + " [SEP]"
    input_ids = tokenizer.encode(input_text)
    token_type_ids = [0 if i <= input_ids.index(102) else 1 for i in range(len(input_ids))]
    start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))
    all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    return (' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores) +1]))

question, text = "How many moods are there?", "My four moods: I'm too old for this shit! I'm too old for this shit! I'm too sober for this shit! I don't have time for this shit!"
print(from_question_return_answer(question, text))

"""