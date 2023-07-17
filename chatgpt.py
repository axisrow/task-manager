import os
import openai
import re

# Открытие файла ключа API
with open('openai.key', 'r') as file:
    api_key = file.read().strip()

# Установка ключа API
openai.api_key = api_key

# Сообщение пользователя
user_message = "Как правильно чистить зубы?"

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "Ты полезный помощник. Сформулируйте ответ в виде списка подзадач, сделав его максимально кратким."},
        {"role": "user", "content": user_message}
    ],
  max_tokens=256
)

# Получение ответа помощника
assistant_message = response["choices"][0]["message"]["content"]

# Разбивка ответа помощника на пункты списка
list_items = assistant_message.split("\n")

# Вывод пунктов списка с удалением лишних цифр в начале каждого пункта
for i, item in enumerate(list_items, 1):
    item = re.sub(r'^\d+\.\s*', '', item)  # Удаление лишних цифр и точки с пробелом
    print(f"{i}. {item}")
