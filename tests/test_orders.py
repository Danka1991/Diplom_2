import allure

from src.api.api_client import ApiClient
from helper import valid_ingredient_hashes, invalid_ingredient_hash
from responses import Responses

class TestOrders:
    @allure.title('Создание заказа с авторизацией и ингридиентами')
    def test_create_order_authorized_with_ingredients(self, api_client: ApiClient, registered_and_authorized_user):
        with allure.step("Получение данных ингредиентов"):
            ing_resp = api_client.get_ingredients()
            ingredient_hashes = valid_ingredient_hashes(ing_resp.json(), limit=3)
        with allure.step("Создание заказа с ингредиентами"):    
            order_resp = api_client.create_order(ingredient_hashes, authorized=True)
        with allure.step("Проверка ответа"):    
            body = order_resp.json()
            assert order_resp.status_code == Responses.CRE_ORDR_INGR_AUTH["code"] and \
                "order" in body and \
                isinstance(body["order"].get("number"), int) and \
                body.get("success") is Responses.CRE_ORDR_INGR_AUTH["success"]

    @allure.title('Создание заказа без авторизациеи')
    def test_create_order_unauthorized(self, api_client: ApiClient):
        with allure.step("Получение данных ингредиентов"):
            ing_resp = api_client.get_ingredients()
            ingredient_hashes = valid_ingredient_hashes(ing_resp.json(), limit=3)
        with allure.step("Создать заказ без авторизации"):    
            order_resp = api_client.create_order(ingredient_hashes, authorized=False)
        with allure.step("Проверить ответ сервера"):    
            body = order_resp.json()
            assert order_resp.status_code == Responses.CRE_ORDR_UNAUTH["code"] and \
                body.get("message") == Responses.CRE_ORDR_UNAUTH["message"] and \
                body.get("success") is Responses.CRE_ORDR_UNAUTH["success"]

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, api_client: ApiClient, registered_and_authorized_user):
        with allure.step("Создать заказ с пустым списком ингредиентов"):    
            order_resp = api_client.create_order([], authorized=True)
        with allure.step("Проверить ответ сервера при отсутствии ингредиентов"):   
            body = order_resp.json()
            assert order_resp.status_code == Responses.CRE_ORDR_NONEINGR_AUTH["code"] and \
                body.get("message") == Responses.CRE_ORDR_NONEINGR_AUTH["message"] and \
                body.get("success") is Responses.CRE_ORDR_NONEINGR_AUTH["success"]

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_invalid_ingredient_hash(self, api_client: ApiClient, registered_and_authorized_user):
        with allure.step("Подготовить неверные хеши ингредиентов"):    
            bad_hashes = [invalid_ingredient_hash()]
        with allure.step("Создать заказ с неверным хешем ингредиентов"):    
            resp = api_client.create_order(bad_hashes, authorized=True)
        with allure.step("Проверить ответ сервера при неверных ингредиентах"):    
            assert resp.status_code == Responses.CRE_ORDR_WRONGINGR_AUTH["code"]
