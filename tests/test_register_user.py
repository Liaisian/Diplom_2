import allure
import requests
import url


class TestRegisterUser:

    @allure.title('Создание уникального пользователя')
    @allure.description('Проверка: статус 201.')
    def test_create_unique_user(self, create_user):
        user_data, response_post = create_user

        assert response_post.status_code == 200
        assert response_post.json()["success"] is True
        assert response_post.json()["user"]["email"] == user_data["email"]
        assert response_post.json()["user"]["name"] == user_data["name"]
        assert 'accessToken' in response_post.json()
        assert 'refreshToken' in response_post.json()


    @allure.title('Cоздание пользователя, который уже зарегистрирован')
    @allure.description('Проверка: статус 403, сообщение об ошибке, что такой уже существует.')
    def test_create_existing_user(self, create_user):
        user_data, _ = create_user

        response = requests.post(f'{url.MAIN_URL}/api/auth/register', data=user_data)

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "User already exists"
        }

    @allure.title('Создание пользователя с отсутствующими полями.')
    @allure.description('Проверка: статус 403, сообщение об ошибке про отсутствие одного из обязательных полей (name, email, password).')
    def test_create_user_missing_fields(self):
        incomplete_data = [
            {"password": "password", "name": "Username"},  # без email
            {"email": "test-data@yandex.ru", "name": "Username"},  # без password
            {"email": "test-data@yandex.ru", "password": "password"},  # без name
        ]

        for data in incomplete_data:
            response_post = requests.post(f'{url.MAIN_URL}/api/auth/register', data=data)
            assert response_post.status_code == 403
            assert response_post.json()["success"] is False
            assert response_post.json()["message"] == "Email, password and name are required fields"


