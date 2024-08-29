import allure
import requests
import url


class TestOrder:

    @allure.title('Авторизованный пользователь может создать заказ')
    @allure.description('Проверка: статус 200, заказ успешно создается.')
    def test_create_order_with_auth(self, create_user, ingredients):
        user_data, response_post = create_user
        token = response_post.json().get('accessToken')

        order_data = {
            "ingredients": [ingredients[0]['_id'], ingredients[1]['_id']]
        }

        response = requests.post(f"{url.MAIN_URL}/api/orders", headers={"Authorization": f"Bearer {token}"}, json=order_data)
        # print(response.text)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True
        assert 'order' in response_data

    @allure.title('Неавторизованный пользователь не может создать заказ')
    @allure.description('Проверка: статус 401, заказ без авторизации нельзя создать.')
    def test_create_order_without_auth(self, ingredients):
        order_data = {
            "ingredients": [ingredients[0]['_id'], ingredients[1]['_id']]
        }

        response = requests.post(f"{url.MAIN_URL}/api/orders", data=order_data)

        assert response.status_code == 401
        response_data = response.json()
        assert response_data.get('success') is False

    @allure.title('Нельзя создать заказ без ингредиентов')
    @allure.description('Проверка: статус 400, Сообщение об ошибке, что необходимо указать ингредиент.')
    def test_create_order_without_ingredients(self, create_user):
        user_data, response_post = create_user
        token = response_post.json().get('accessToken')

        order_data = {}

        response = requests.post(f"{url.MAIN_URL}/api/orders", headers={"Authorization": f"Bearer {token}"}, json=order_data)

        assert response.status_code == 400
        response_data = response.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == "Ingredient ids must be provided"

    @allure.title('Нельзя создать заказ с невалидным хешем ингредиента')
    @allure.description('Проверка: статус 500, Internal Server Error.')
    def test_create_order_with_invalid_ingredient_hash(self, create_user):
        user_data, response_post = create_user
        token = response_post.json().get('accessToken')

        order_data = {
            "ingredients": ["invalid_hash_1", "invalid_hash_2"]
        }

        response = requests.post(f"{url.MAIN_URL}/api/orders", headers={"Authorization": f"Bearer {token}"}, json=order_data)

        assert response.status_code == 500

    @allure.title('Получение заказа авторизованного пользователя')
    @allure.description('Проверка: статус 200, в ответе те ингридиенты, что отправлялись в запросе.')
    def test_get_orders_with_auth(self, create_user):
        user_data, response_post = create_user
        token = response_post.json().get('accessToken')

        response = requests.get(f"{url.MAIN_URL}/api/orders", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get('success') is True

    @allure.title('Получение заказа неавторизованного пользователя')
    @allure.description('Проверка: статус 401, сообщение с ошибкой.')
    def test_get_orders_without_auth(self):
        response = requests.get(f"{url.MAIN_URL}/api/orders")

        assert response.status_code == 401
        response_data = response.json()
        assert response_data.get('success') is False

