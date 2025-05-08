import json

def find_answer_indices(context, answer):
    start_index = context.find(answer)
    return start_index

# Load the dataset from the JSON file
# with open('../../vta_qa_model/training/faqs.json', 'r') as data:
with open('vta_qa_model/training/newdataset/vista.json', 'r',encoding="utf-8") as data:
    dataset = json.load(data)
counter = 0
# Iterate through each item in the dataset
for item in dataset:
    context = item["context"]
    qas = item["qas"]
    print("Context:", context)

    # Iterate through each question-answer pair (qas)
    for qa in qas:
        question = qa["question"]
        answers = qa["answers"]
        counter += 1

        # Iterate through each answer in the answers list
        for answer in answers:
            # Check if "answer_start" key is present in the answer
            if "answer_start" in answer:
                # Find the start index of the answer in the context
                start_index = find_answer_indices(context, answer["text"][0])
                if start_index != -1:
                    # Update the "answer_start" field in the answer
                    answer["answer_start"] = start_index
                    answer["answer_end"] = start_index + len(answer["text"][0])
                    print("Answer:", answer["text"])
                    print("Starting index:", start_index)
                    print("Ending index:", start_index)
                else:
                    print("Answer not found in context.")
                    # Set answer_start to -1 to indicate answer not found
                    answer["answer_start"] = -1  

# Write the updated dataset back to the JSON file
# with open('../../vta_qa_model/training/faqs.json', 'w') as data:
with open('vta_qa_model/training/newdataset/vista.json', 'w') as data:
    json.dump(dataset, data, indent=4)
print("counter: ",counter)