import random
import string


#Генерируем случайную строку заданной длины
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

#Создаем нового пользователя и возвращаем его данные
def generate_user_data():
    email = generate_random_string(5) + "@yandex.ru"
    password = generate_random_string(10)
    name = generate_random_string(10)

    return {
        "email": email,
        "password": password,
        "name": name
    }


