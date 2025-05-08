import json

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def save_qa_pairs_to_json(qa_pairs, file_path):
    with open(file_path, 'w') as f:
        json.dump(qa_pairs, f, indent=4)

# data1 = read_json_file('invalid_qa_pairs.json')
# data2 = read_json_file('valid_qa_pairs.json')
# data = data1 + data2

data= read_json_file('mix.json')
invalid_qa_pairs = []


correct_predictions = 0

for entry in data:
    predicted_answer = entry["predicted_answer"]
    true_answer = entry["true_answer"]
    
    # if predicted_answer in true_answer:
    if  predicted_answer  and (true_answer in predicted_answer  or predicted_answer in true_answer) :
    # if true_answer in predicted_answer:
        correct_predictions += 1
    else:
        invalid_qa_pairs.append({
                'question': entry["question"],
                'predicted_answer': entry["predicted_answer"],
                'true_answer':  true_answer
                })
   
save_qa_pairs_to_json(invalid_qa_pairs,'mixup.json')
total_predictions = len(data)
percentage_correct = (correct_predictions / total_predictions) * 100

print(f"Correct predictions: {correct_predictions}")
print(f"Total predictions: {total_predictions}")
print(f"Percentage of correct predictions: {percentage_correct:.2f}%")
