import allure
import requests
from helpers import generate_user_data
import url


class TestUser:
    @allure.title('Успешное изменение данных авторизованного пользователя')
    @allure.description('Проверка: статус 200, данные успешно меняются и возвращаются в ответе.')
    def test_update_user_with_auth(self, create_user):
        user_data, response_post = create_user
        token = response_post.json()['accessToken']

        # Обновление данных пользователя
        new_data = {
            "email": generate_user_data()['email'],
            "name": generate_user_data()['name']
        }

        response = requests.patch(f"{url.MAIN_URL}/api/auth/user", headers={"Authorization": f"Bearer {token}"}, json=new_data)

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['user']['email'] == new_data['email']
        assert response.json()['user']['name'] == new_data['name']

    @allure.title('Неавторизованный пользователь не может изменить свои данные')
    @allure.description('Проверка: статус 401, сообщение об ошибке при попытке изменения данных неавторизованным пользователем.')
    def test_update_user_without_auth(self, create_user):
        user_data, _ = create_user
        # Обновление данных пользователя без авторизации
        response = requests.patch(f"{url.MAIN_URL}/api/auth/user", json=user_data)

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == "You should be authorised"

