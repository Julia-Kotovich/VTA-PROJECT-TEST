from .helper import process_data_for_context_finder, get_context, find_best_qa_pair
from transformers import BertForQuestionAnswering, BertTokenizer, AutoTokenizer
import torch
import re
import random


class VTA:
    def __init__(self,
                 model,tokenizer,context_path):
        self.model = model
        self.tokenizer = tokenizer
        self.contexts = process_data_for_context_finder(context_path)


    def validate_input(self, user_query):
        # Заменяем типографские кавычки на обычные
        query = user_query.replace('’', "'")
        query = query.replace('"', '"')
        query = query.replace('"', '"')
        query = query.rstrip('?')
        print('query after stripping: ', query)
        # Check if input is too long or too short
        if len(query) > 300 or len(query) < 3:
            return False
        # Check for repeated characters
        if re.match(r'(.)\1{4,}', query):
            return False
        # Разрешаем буквы, цифры, пробелы и основные знаки препинания
        if not re.match(r'^[\w\s\.,;:!\?\'"()\-–—/\\]+$', query):
            return False
        # Check for nonsensical patterns
        if re.match(r'^[\da-zA-Z]+$', query):
            return False
        return True



    def answer_question(self, question):
        if not self.validate_input(question):
            print('validator:', self.validate_input(question))
            return "I'm sorry, I couldn't quite understand your question. Could you please rephrase or clarify it?"

        # Новый поиск по всем вопросам-ответам
        # Путь к датасету (можно вынести в переменную класса)
        dataset_path = 'vta_qa_model/training/newdataset/vista.json'
        best_q, best_a, best_score = find_best_qa_pair(question, dataset_path)
        print(f'[DEBUG] Best match question: {best_q}')
        print(f'[DEBUG] Best match answer: {best_a}')
        print(f'[DEBUG] Similarity score: {best_score}')
        if best_score > 0.3:
            return best_a

        # fallback: старая логика (поиск по контексту)
        context, similarity_score = get_context(question, self.contexts)
        input = self.tokenizer(context, question, return_tensors="pt", padding=True)
        output = self.model(**input)
        start_index = output.start_logits.argmax()
        end_logits = output.end_logits.squeeze()
        max_end_logit = end_logits[start_index].item()
        end_index = start_index
        for i, logit in enumerate(end_logits[start_index:], start=start_index):
            if logit > max_end_logit:
                max_end_logit = logit
                end_index = i
        model_answer = self.tokenizer.decode(input.input_ids[0, start_index:end_index])
        if similarity_score < 0.1:
            responses = [
                'Unfortunately, I do not have an answer to your question. Please rephrase your question. Remember I can only provide you information about the Capstone Project Course at Constructor Institute of Technology.',
                'Unfortunately, I didn\'t understand your question. Please rephrase your question. Remember I can only provide you information about the Capstone Project Course at Constructor Institute of Technology.',
                'Unfortunately, I wasn\'t able to fully understand your question. Please rephrase your question. Remember I can only provide you information about the Capstone Project Course at Constructor Institute of Technology.'
            ]
            random_answer_index = random.randint(0, len(responses) - 1)
            return responses[random_answer_index] + 'Please rephrase your question.'
        return model_answer
    
    
    

# if __name__ == "__main__":
#     model_name = "bert-large-uncased-whole-word-masking-finetuned-squad" 
#     model_path = "./vta_qa_model/model/vta_model_bert_v4"
#     tokenizer = BertTokenizer.from_pretrained(model_path)
#     context_path = './training/val-data.json'
#     model = BertForQuestionAnswering.from_pretrained(model_path)
#     vta = VTA(model,tokenizer,context_path)

#     print("VTA: Hi! I'm your Virtual Assistant For Capstone. How may I help you?")
#     while True:
#         user_question = input("You: ")
#         if user_question.lower() == 'exit':
#             print("VTA: Goodbye!")
#             break
        
#         answer = vta.answer_question(user_question)

#         print("VTA:", answer)

