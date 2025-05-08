import json
import os

def convert_json_to_markdown(input_file, output_file):
    # Читаем JSON файл
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Подсчитываем статистику
    total_questions = 0
    unique_questions = set()
    total_answers = 0
    
    for context_data in data:
        qas = context_data['qas']
        total_questions += len(qas)
        for qa in qas:
            unique_questions.add(qa['question'])
            total_answers += len(qa['answers'])
    
    # Создаем Markdown файл
    with open(output_file, 'w', encoding='utf-8') as f:
        # Заголовок и статистика
        f.write("# QA Dataset Overview\n\n")
        f.write("## Dataset Statistics\n\n")
        f.write(f"- Total contexts: {len(data)}\n")
        f.write(f"- Total questions: {total_questions}\n")
        f.write(f"- Unique questions: {len(unique_questions)}\n")
        f.write(f"- Total answers: {total_answers}\n")
        f.write(f"- Average questions per context: {total_questions/len(data):.2f}\n")
        f.write(f"- Average answers per question: {total_answers/total_questions:.2f}\n\n")
        
        # Счетчик для нумерации пар
        pair_counter = 1
        
        # Для каждого контекста
        for context_data in data:
            context = context_data['context']
            qas = context_data['qas']
            
            # Записываем контекст
            f.write(f"## Context {pair_counter}\n\n")
            f.write(f"**Context Text:**\n{context}\n\n")
            
            # Записываем вопросы и ответы
            f.write("### Questions and Answers:\n\n")
            for qa in qas:
                question = qa['question']
                answers = qa['answers']
                
                f.write(f"#### Question {pair_counter}.{qa['id']}\n")
                f.write(f"**Q:** {question}\n\n")
                
                for answer in answers:
                    f.write(f"**A:** {answer['text'][0]}\n")
                    f.write(f"*Answer position:* {answer['answer_start']} - {answer['answer_end']}\n\n")
            
            f.write("---\n\n")
            pair_counter += 1

if __name__ == "__main__":
    # Пути к файлам
    input_file = "vta_qa_model/training/newdataset/vista.json"
    output_file = "vta_qa_model/training/newdataset/vista.md"
    
    # Конвертируем
    convert_json_to_markdown(input_file, output_file)
    print(f"Conversion complete! Markdown file saved to {output_file}") 