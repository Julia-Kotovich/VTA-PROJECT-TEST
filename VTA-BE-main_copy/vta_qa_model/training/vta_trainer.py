from transformers import BertTokenizerFast, BertForQuestionAnswering, AdamW, TrainingArguments, Trainer, pipeline
import torch
from torch.utils.data import DataLoader
import json
from huggingface_hub import login
from transformers import AdamW,get_linear_schedule_with_warmup
from tqdm import tqdm
import random
from squad_dataset import SquadDataset


class VTAQAModel:
    def __init__(
        self,
        model_checkpoint,
        n_best=20,
        num_train_epochs=4,
        output_dir="model/vta_model_bert_7alpha1",
        train_size=0.8,
        batch_size = 16       
            ):
        self.model_checkpoint = model_checkpoint
        self.tokenizer = BertTokenizerFast.from_pretrained(model_checkpoint)
        self.n_best = n_best
        self.num_train_epochs = num_train_epochs
        self.output_dir = output_dir
        self.train_size = train_size
        self.batch_size = batch_size
        
    # load data from json file
    def load_data(self,file_path,size = None):
        dataset = []
        with open(file_path) as data:
            dataset = json.load(data) 
        # return all data if size is none or not a valid percentage  
        if size is None or size <= 0 or size > 100:
            return dataset
        num_of_data = int((size / 100) * len(dataset))
        return dataset[:num_of_data]
 
    def process_data(self,data_set):
        contexts = []
        questions = []
        answers = []

        for item in data_set:
            context = item["context"]
            for qa in item["qas"]:
                question = qa["question"]
               
                for ans in qa['answers']:
                    contexts.append(context)
                    questions.append(question)
                    answers.append(ans)
                           
        return contexts,questions,answers
    
    def add_answer_end_indices(self,answers,contexts):
        for answer,context in zip(answers,contexts):
            gold_text = answer['text'][0]
            start_index = answer['answer_start']
            end_index = start_index + len(gold_text)
            answer['answer_end'] = end_index
    
    def add_token_positions(self,encodings,answers):
        start_positions = []
        end_positions = []
        for i in range(len(answers)):
            start_positions.append(encodings.char_to_token(i,answers[i]['answer_start']))
            end_positions.append(encodings.char_to_token(i,answers[i]['answer_end']))
            if start_positions[-1] is None:
                start_positions[-1] = tokenizer.model_max_length
            go_back = 1
            while end_positions[-1] is None:
                end_positions[-1] = encodings.char_to_token(i,answers[i]['answer_end']-go_back)
                go_back += 1

        encodings.update({
            'start_positions' : start_positions,
            'end_positions' : end_positions
        })

    
    def finetune(self,model,train_loader):
        device = torch.device('cpu')
        model.to(device)
        model.train()
        optim = AdamW(model.parameters(),lr=3e-5,weight_decay=0.01)

        # Calculate the total number of training steps
        total_steps = len(train_loader) * self.num_train_epochs
        
        # Calculate the number of warmup steps
        warmup_steps = int(0.1 * total_steps)
        
        # Define the learning rate scheduler
        scheduler = get_linear_schedule_with_warmup(
            optim, 
            num_warmup_steps=warmup_steps, 
            num_training_steps=total_steps
        )

        for epoch in range(self.num_train_epochs):
            loop =  tqdm(train_loader)
            
            for batch in loop:
                optim.zero_grad()

                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                start_positions = batch['start_positions'].to(device)
                end_positions = batch['end_positions'].to(device)

                outputs = model(input_ids,attention_mask = attention_mask,start_positions = start_positions,end_positions = end_positions)

                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

                loss = outputs[0]
                loss.backward()
                optim.step()
                scheduler.step()

                loop.set_description(f'Epoch {epoch + 1}/{self.num_train_epochs}')
                loop.set_postfix(loss = loss.item())


        model.save_pretrained(self.output_dir)
        tokenizer.save_pretrained(self.output_dir)
        model.eval()

    def perform_validation(self,model,val_loader):
        device = torch.device('cpu')
        model.to(device)
        acc = []
        loop =  tqdm(val_loader)
        
        for batch in loop:
            with torch.no_grad():
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                start_true = batch['start_positions'].to(device)
                end_true = batch['end_positions'].to(device)

                outputs = model(input_ids,attention_mask = attention_mask)
                start_pred = torch.argmax(outputs['start_logits'],dim = 1)
                end_pred = torch.argmax(outputs['end_logits'],dim = 1)
                acc.append(((start_pred == start_true).sum()/len(start_pred)).item())
                acc.append(((end_pred == end_true).sum()/len(end_pred)).item())

        # print accuracy
        print('accuracy',sum(acc)/len(acc))
        print(acc)



   
if __name__ == "__main__":
    checkpoint = 'bert-base-uncased'

    tokenizer = BertTokenizerFast.from_pretrained(checkpoint)
    vta_model = VTAQAModel(checkpoint)
  
    train_file_path = 'newdataset/vista.json'
    val_file_path = 'newdataset/vista.json'

    train_data = vta_model.load_data(train_file_path)
    val_data = vta_model.load_data(val_file_path)

    train_contexts,train_questions, train_answers = vta_model.process_data(train_data)
    val_contexts,val_questions, val_answers = vta_model.process_data(val_data)
    vta_model.add_answer_end_indices(train_answers,train_contexts)
    vta_model.add_answer_end_indices(val_answers,val_contexts)

  
    train_encodings = tokenizer(train_contexts, train_questions, truncation=True, padding=True)
    val_encodings = tokenizer(val_contexts, val_questions, truncation=True, padding=True)

    # add start and end positon tokens
    vta_model.add_token_positions(train_encodings,train_answers)
    vta_model.add_token_positions(val_encodings,val_answers)
    
    train_dataset= SquadDataset(train_encodings)
    val_dataset= SquadDataset(val_encodings)

    # Training
    # checkpoint = 'bert-base-uncased'
    checkpoint = '../model/vta_model_bert_v7'
    tokenizer = BertTokenizerFast.from_pretrained(checkpoint)
    model = BertForQuestionAnswering.from_pretrained(checkpoint)

    # perform finetuning
    # train_loader = DataLoader(train_dataset,batch_size=16,shuffle=True)
    train_loader = DataLoader(train_dataset,batch_size=8,shuffle=True)
    vta_model.finetune(model,train_loader)

    # perform validation
    # checkpoint = './model/vta_model_bert_v1'
    # tokenizer = BertTokenizerFast.from_pretrained(checkpoint)
    # model = BertForQuestionAnswering.from_pretrained(checkpoint)
    # val_loader = DataLoader(val_dataset,batch_size=16,shuffle=True)
    # vta_model.perform_validation(model,val_loader);





   