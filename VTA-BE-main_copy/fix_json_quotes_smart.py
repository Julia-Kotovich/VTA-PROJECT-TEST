import json

# Загружаем исходный файл
with open('vista_pitch_block.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Функция для экранирования кавычек внутри строки
fix = lambda s: s.replace('"', '\"') if isinstance(s, str) else s

# Проходим по всем вопросам и ответам
for qa in data.get('qas', []):
    if 'question' in qa:
        qa['question'] = fix(qa['question'])
    for ans in qa.get('answers', []):
        if 'text' in ans and isinstance(ans['text'], list):
            ans['text'] = [fix(t) for t in ans['text']]

# Сохраняем исправленный файл
with open('vista_pitch_block_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Готово! Проверь файл vista_pitch_block_fixed.json') 