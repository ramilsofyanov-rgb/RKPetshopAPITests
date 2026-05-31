import allure
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_create_order(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url= f"{BASE_URL}/store/order", json= payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка, что ответ содержит данные заказа"):
            response.data = response.json()
            assert response.data["id"] == payload["id"], "id заказа не совпадает с ожидаемым"
            assert response.data["petId"] == payload["petId"],"petId заказа не совпадает с ожидаемым"
            assert response.data["quantity"] == payload["quantity"], "quantity заказа не совпадает с ожидаемым"
            assert response.data["status"] == payload["status"], "status заказа не совпадает с ожидаемым"
            assert response.data["complete"] == payload["complete"], "complete заказа не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self):
        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url= f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка, что ответ содержит данные заказа с id = 1"):
            assert response.json()["id"] == 1

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self):
        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(url= f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка запроса на получение информации о удаленном заказе"):
            response = requests.get(url= f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url= f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря"):
            response = requests.get(url= f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка, что ответ содержит данные инвентаря"):
            data = response.json()
            assert type(data["approved"]) == int
            assert type(data["delivered"]) == int

