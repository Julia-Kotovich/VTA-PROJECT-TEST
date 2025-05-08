import re
import json

input_file = 'pitch_demo_q&a.txt'
output_file = 'training_data.json'

with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Ищем пары вопрос-ответ
pairs = re.findall(r'Q\d+\. (.*?)\nA\d+\. (.*?)(?=\nQ\d+\.|$)', text, re.DOTALL)

data = [{"question": q.strip(), "answer": a.strip()} for q, a in pairs]

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Готово! Найдено пар: {len(data)}. Результат сохранён в {output_file}') 