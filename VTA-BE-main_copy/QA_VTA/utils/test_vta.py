import json

from transformers import BertForQuestionAnswering, BertTokenizer, AutoTokenizer
import torch
import os

from qa_vta_test import VTA


def find_answer_indices(context, answer):
    start_index = context.find(answer)
    return start_index


# model_name = "bert-large-uncased-whole-word-masking-finetuned-squad" 
# model_path = "../vta_qa_model/model/vta_model_bert_v7"
# tokenizer = BertTokenizer.from_pretrained(model_path)
# context_path = '../vta_qa_model/training/newdataset-sc/singlecontext-clean.json'
# model = BertForQuestionAnswering.from_pretrained(model_path)

model_path = os.path.abspath('../vta_qa_model/model/vta_model_bert_v6')
tokenizer = BertTokenizer.from_pretrained(model_path)
context_path = os.path.abspath('../vta_qa_model/training/newdataset/singlecontext.json')
model = BertForQuestionAnswering.from_pretrained(model_path)

vta = VTA(model,tokenizer,context_path)


# Load the dataset from the JSON file
with open(context_path, 'r') as data:
    dataset = json.load(data)
counter = 0
# Iterate through each item in the dataset
for item in dataset[:50]:
    c = item["context"]
    qas = item["qas"]
    # print("Context:", context)
    print('-------- start of context ------------------')

    # Iterate through each question-answer pair (qas)
    for qa in qas:
        q = qa["question"]
        answers = qa["answers"]
      
        bot_response = vta.answer_question(q,c)
                # start_index = find_answer_indices(context, bot_response)
                # if start_index != -1:                    
                    
        print("Bot response: ", bot_response)
        print('------------------- end of context -------------------------------')
 
                     

# # Write the updated dataset back to the JSON file
# with open('./training/train-datacls.json', 'w') as data:
#     json.dump(dataset, data, indent=4)
