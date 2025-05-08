from sklearn.metrics import precision_recall_fscore_support
import torch
from tqdm import tqdm
from transformers import BertTokenizerFast, BertForQuestionAnswering, AdamW, TrainingArguments, Trainer, pipeline
from torch.utils.data import DataLoader,random_split
from vta_trainer import VTAQAModel
from squad_dataset import SquadDataset

def perform_validation(model, val_loader):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    em, f1 = [], []
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
                    
                    em.append(1)
                else:
                    em.append(0)

                f1_score = compute_f1(pred_answer, true_answer)
                f1.append(f1_score)
    
    # Print metrics
    print(f'Exact Match: {sum(em) / len(em):.4f}')
    print(f'F1 Score: {sum(f1) / len(f1):.4f}')

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
  
val_file_path = './newdataset/vista.json'

val_data = vta_model.load_data(val_file_path)
val_contexts,val_questions, val_answers = vta_model.process_data(val_data)
vta_model.add_answer_end_indices(val_answers,val_contexts)
val_encodings = tokenizer(val_contexts, val_questions, truncation=True, padding=True)

# add start and end positon tokens
vta_model.add_token_positions(val_encodings,val_answers)

val_dataset= SquadDataset(val_encodings)
# val_size = int(0.2 * len(val_dataset))
# _, val_dataset = random_split(val_dataset, [len(val_dataset) - val_size, val_size])


checkpoint = '../model/vta_model_bert_7alpha'
tokenizer = BertTokenizerFast.from_pretrained(checkpoint)
model = BertForQuestionAnswering.from_pretrained(checkpoint)
vl = DataLoader(val_dataset,batch_size=8,shuffle=True)
perform_validation(model,vl);