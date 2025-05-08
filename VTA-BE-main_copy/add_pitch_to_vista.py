import json

# Читаем исходные данные
with open('training_data_pitch.json', 'r', encoding='utf-8') as f:
    pitch_data = json.load(f)

qas = []
for idx, item in enumerate(pitch_data, 1):
    question = item['question']
    answer = item['answer']
    qas.append({
        "id": f"pitch_{idx:03}",
        "is_impossible": False,
        "question": question,
        "answers": [
            {
                "text": [answer],
                "answer_start": 0,
                "answer_end": len(answer)
            }
        ]
    })

pitch_block = {
    "context": "pitch",
    "qas": qas
}

# Сохраняем результат в новый файл
with open('vista_pitch_block.json', 'w', encoding='utf-8') as f:
    json.dump(pitch_block, f, ensure_ascii=False, indent=2)

print(f"Готово! Создан файл vista_pitch_block.json с {len(qas)} парами.") 