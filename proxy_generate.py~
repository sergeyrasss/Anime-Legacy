# Чтение содержимого файла
with open('grand_blue_images.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Разделение содержимого на строки
lines = [line.strip() for line in content.split('\n') if line.strip()]

# Преобразование каждой строки
modified_lines = []
for line in lines:
    if line.startswith('https://img4.desu.city'):
        # Генерация DuckDuckGo прокси-ссылки
        proxy_url = f'https://proxy.duckduckgo.com/iu/?u={line}'
        modified_lines.append(proxy_url)
    else:
        modified_lines.append(line)

# Объединение строк обратно
modified_content = '\n'.join(modified_lines)

# Запись измененного содержимого обратно в файл
with open('grand_blue_images_modified.txt', 'w', encoding='utf-8') as file:
    file.write(modified_content)

print("Файл успешно изменен и сохранен как 'grand_blue_images_modified.txt'")
print(f"Обработано {len(modified_lines)} ссылок (только DuckDuckGo прокси)")