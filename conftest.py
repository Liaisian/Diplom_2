import helpers
import url
from helpers import generate_user_data
import pytest
import requests


@pytest.fixture
def create_user():
    #Генерируем пользователя
    user_data = helpers.generate_user_data()
    # Создаем пользователя
    response_post = requests.post(f'{url.MAIN_URL}/api/auth/register', data=user_data)
    access_token = response_post.json()["accessToken"]
    headers = {
        "Content-type": "application/json",
        "Authorization": f'{access_token}'
    }
    yield user_data, response_post

    # Удаление пользователя после теста
    requests.delete(f'{url.MAIN_URL}/api/auth/user', headers=headers)

@pytest.fixture()
def ingredients():
    response = requests.get(f"{url.MAIN_URL}/ingredients")
    return response.json()['data']

