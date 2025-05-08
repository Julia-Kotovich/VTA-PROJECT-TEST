from transformers import BertTokenizerFast, BertForQuestionAnswering, AdamW, TrainingArguments, Trainer, pipeline
import torch
import json
from huggingface_hub import login
from decouple import config
from indexfinder import find_answer_indices


# Load tokenizer and model
checkpoint = 'bert-base-uncased'
tokenizer = BertTokenizerFast.from_pretrained(checkpoint)
model = BertForQuestionAnswering.from_pretrained(checkpoint)
qa_pipeline = pipeline("question-answering", model=checkpoint, tokenizer=checkpoint)


# Tokenized dataset
tokenized_dataset = []
with open('./training/data-1-CH23.json') as data:
    dataset = json.load(data)


for item in dataset:
    context = item["context"]
    questions = item["qas"]
   
    # Tokenize the context
    tokenized_context = tokenizer(context, padding=True, truncation=True, return_tensors="pt")
    
    # Process each question and its response
    for question in questions:
        user_query = question["user_query"]
        vat_response = question["vat_response"]
        start_index, end_index = find_answer_indices(context,question["vat_response"]) 
    
        
        # Tokenize the user query
        tokenized_query = tokenizer(user_query, padding=True, truncation=True,return_tensors="pt")
   
        # Append the tokenized context and query along with the expected response to the tokenized dataset
        tokenized_dataset.append({
            "input_ids": tokenized_context.input_ids.flatten(),
            "attention_mask": tokenized_context.attention_mask.flatten(),
            "question_input_ids": tokenized_query.input_ids.flatten(),
            "question_attention_mask": tokenized_query.attention_mask.flatten(),
            "response": vat_response,
            "start_positions": start_index,
            "end_positions": end_index, 
        })



api_key = config('HUGGINGFACE_API_KEY')
# Interactive prompt to log in
login(api_key)

# Define training arguments
training_args = TrainingArguments(
    output_dir="vta_model",
    evaluation_strategy="no",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Define Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
)

# Start training
trainer.train()

# save model
trainer.save_model("vta_saved")
