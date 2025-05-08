from sklearn.metrics import precision_recall_fscore_support
import torch
from tqdm import tqdm
from transformers import BertTokenizerFast, BertForQuestionAnswering, AdamW, TrainingArguments, Trainer, pipeline
from torch.utils.data import DataLoader,random_split
from vta_qa_model.training.vta_trainer import VTAQAModel
from vta_qa_model.training.squad_dataset import SquadDataset
import json

def perform_validation(model, val_loader,tokenizer):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    em, f1 = [], []
    qa_pairs = []
    invalid_qa_pairs = []
    loop = tqdm(val_loader)
    
    for batch in loop:
        with torch.no_grad():
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            start_true = batch['start_positions'].to(device)
            end_true = batch['end_positions'].to(device)

            outputs = model(input_ids, attention_mask=attention_mask)
            start_pred = torch.argmax(outputs['start_logits'], dim=1)
            end_pred = torch.argmax(outputs['end_logits'], dim=1)

            for i in range(len(start_true)):
                pred_answer = (start_pred[i].item(), end_pred[i].item())
                true_answer = (start_true[i].item(), end_true[i].item())

                if pred_answer == true_answer:
                    input_id = input_ids[i].tolist()
                    pred_text = tokenizer.decode(input_id[start_pred[i]:end_pred[i]+1])
                    true_text = tokenizer.decode(input_id[start_true[i]:end_true[i]+1])
                    
                    question = tokenizer.decode(input_id, skip_special_tokens=True, clean_up_tokenization_spaces=True)
                    
                    qa_pairs.append({
                        'question': question,
                        'predicted_answer': pred_text,
                        'true_answer': true_text
                    })
                    em.append(1)
                else:
                    input_id = input_ids[i].tolist()
                    pred_text = tokenizer.decode(input_id[start_pred[i]:end_pred[i]+1])
                    true_text = tokenizer.decode(input_id[start_true[i]:end_true[i]+1])
                    
                    question = tokenizer.decode(input_id, skip_special_tokens=True, clean_up_tokenization_spaces=True)
                    invalid_qa_pairs.append({
                    'question': question,
                    'predicted_answer': pred_text,
                    'true_answer': true_text
                    })

                    em.append(0)

                f1_score = compute_f1(pred_answer, true_answer)
                f1.append(f1_score)
    
    # Print metrics
    print(f'Exact Match: {sum(em) / len(em):.4f}')
    print(f'F1 Score: {sum(f1) / len(f1):.4f}')
    return qa_pairs, invalid_qa_pairs

def save_qa_pairs_to_json(qa_pairs, file_path):
    with open(file_path, 'w') as f:
        json.dump(qa_pairs, f, indent=4)
def compute_f1(pred, true):
    pred_start, pred_end = pred
    true_start, true_end = true
    
    pred_tokens = set(range(pred_start, pred_end + 1))
    true_tokens = set(range(true_start, true_end + 1))

    common_tokens = pred_tokens.intersection(true_tokens)
    if not common_tokens:
        return 0.0
    precision = len(common_tokens) / len(pred_tokens)
    recall = len(common_tokens) / len(true_tokens)
    
    return 2 * (precision * recall) / (precision + recall)


# perform validation

checkpoint = 'bert-base-uncased'
tokenizer = BertTokenizerFast.from_pretrained(checkpoint)
vta_model = VTAQAModel(checkpoint)
  
val_file_path = './training/newdataset/vista.json'

val_data = vta_model.load_data(val_file_path)
val_contexts,val_questions, val_answers = vta_model.process_data(val_data)
vta_model.add_answer_end_indices(val_answers,val_contexts)
val_encodings = tokenizer(val_contexts, val_questions, truncation=True, padding=True)

# add start and end positon tokens
vta_model.add_token_positions(val_encodings,val_answers)

val_dataset= SquadDataset(val_encodings)
# val_size = int(0.2 * len(val_dataset))
# _, val_dataset = random_split(val_dataset, [len(val_dataset) - val_size, val_size])


checkpoint = './model/vta_model_bert_7alpha'
tokenizer = BertTokenizerFast.from_pretrained(checkpoint)
model = BertForQuestionAnswering.from_pretrained(checkpoint)
vl = DataLoader(val_dataset,batch_size=8,shuffle=True)
qa_pairs , invalid_qa_pairs = perform_validation(model,vl,tokenizer);


# save valid and invalid qa_pairs
"""
   The json results has the keys question,predicted_answer, true_answer
   question: holds the context and the question. the question can be found at the end of the context
   predicted_answer: field holds the model's predicted answer
   true_answer: the ground true answer used for training
"""
save_qa_pairs_to_json(qa_pairs,'valid_qa_pairs.json')
save_qa_pairs_to_json(invalid_qa_pairs,'invalid_qa_pairs.json')