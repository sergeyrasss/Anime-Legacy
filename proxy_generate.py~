# Чтение содержимого файла
with open('grand_blue_images.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Разделение содержимого на строки
lines = content.split('\n')

# Преобразование каждой строки
modified_lines = []
for line in lines:
    if line.startswith('https://img4.desu.city'):
        # Удаление 'https://' и добавление нового префикса
        modified_line = 'https://images.weserv.nl/?url=' + line[8:]
        modified_lines.append(modified_line)
    else:
        modified_lines.append(line)

# Объединение строк обратно
modified_content = '\n'.join(modified_lines)

# Запись измененного содержимого обратно в файл
with open('grand_blue_images_modified.txt', 'w', encoding='utf-8') as file:
    file.write(modified_content)

print("Файл успешно изменен и сохранен как 'grand_blue_images_modified.txt'")