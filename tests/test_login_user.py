import requests
import allure
import url


class TestLoginUser:
    @allure.title('Логин под существующим пользователем')
    @allure.description('Проверка успешного логина: статус 200; email и имя в ответе совпадают с отправленными')
    def test_login_existing_user(self, create_user):
        user_data, _ = create_user

        # Логинимся под существующим пользователем
        login_response = requests.post(f'{url.MAIN_URL}/api/auth/login', json={
            "email": user_data["email"],
            "password": user_data["password"]
        })

        assert login_response.status_code == 200
        assert login_response.json()["success"] is True
        assert "accessToken" in login_response.json()
        assert "refreshToken" in login_response.json()
        assert login_response.json()["user"]["email"] == user_data["email"]
        assert login_response.json()["user"]["name"] == user_data["name"]


    @allure.title('Логин с неверным логином и паролем')
    @allure.description('Проверка:статус 401, сообщение об ошибке о некорректных данных.')
    def test_login_with_incorrect_credentials(self):
        # Логинимся с неверным логином и паролем
        invalid_credentials = [
            {"email": "nonexistent@yandex.ru", "password": "wrongpassword"},  # Неверный email
            {"email": "test@yandex.ru", "password": "wrongpassword"},  # Неверный пароль
            {"email": "", "password": "password"},  # Пустой email
            {"email": "test@yandex.ru", "password": ""},  # Пустой пароль
        ]

        for credentials in invalid_credentials:
            login_response = requests.post(f'{url.MAIN_URL}/api/auth/login', json=credentials)
            assert login_response.status_code == 401
            assert login_response.json()["success"] is False
            assert login_response.json()["message"] == "email or password are incorrect"





