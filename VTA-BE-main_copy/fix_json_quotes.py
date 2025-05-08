import re

# Читаем исходный файл как текст
with open('vista_pitch_block.json', 'r', encoding='utf-8') as f:
    text = f.read()

# Функция для экранирования двойных кавычек внутри строковых значений
# (не трогаем кавычки, которые открывают/закрывают ключи и значения)
def fix_quotes(s):
    # Экранируем только те кавычки, которые находятся внутри строк
    # Используем регулярку для поиска кавычек внутри значений
    def replacer(match):
        value = match.group(0)
        # Экранируем все " внутри значения, кроме уже экранированных
        fixed = re.sub(r'(?<!\\)"', r'\\"', value)
        return fixed
    # Ищем все значения строк ("..."), внутри которых есть неэкранированные кавычки
    return re.sub(r':\s*"([^"]*?"[^"]*?)"', lambda m: ': "' + m.group(1).replace('"', '\\"') + '"', s)

fixed_text = fix_quotes(text)

# Сохраняем исправленный файл
with open('vista_pitch_block_fixed.json', 'w', encoding='utf-8') as f:
    f.write(fixed_text)

print('Готово! Проверь файл vista_pitch_block_fixed.json') 