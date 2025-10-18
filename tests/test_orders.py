import allure

from src.api.api_client import ApiClient
from helper import valid_ingredient_hashes, invalid_ingredient_hash
from responses import Responses

class TestOrders:
    @allure.title('Создание заказа с авторизацией и ингридиентами')
    def test_create_order_authorized_with_ingredients(self, api_client: ApiClient, registered_user):
        login_resp = api_client.login(registered_user["email"], registered_user["password"])
        ing_resp = api_client.get_ingredients()
        ingredient_hashes = valid_ingredient_hashes(ing_resp.json(), limit=3)
        order_resp = api_client.create_order(ingredient_hashes, authorized=True)
        body = order_resp.json()
        assert order_resp.status_code == Responses.CRE_ORDR_INGR_AUTH["code"] and \
            "order" in body and \
            isinstance(body["order"].get("number"), int) and \
            body.get("success") is Responses.CRE_ORDR_INGR_AUTH["success"]

    @allure.title('Создание заказа без авторизациеи')
    def test_create_order_unauthorized(self, api_client: ApiClient):
        ing_resp = api_client.get_ingredients()
        ingredient_hashes = valid_ingredient_hashes(ing_resp.json(), limit=3)
        order_resp = api_client.create_order(ingredient_hashes, authorized=False)
        body = order_resp.json()
        assert order_resp.status_code == Responses.CRE_ORDR_UNAUTH["code"] and \
            body.get("message") == Responses.CRE_ORDR_UNAUTH["message"] and \
            body.get("success") is Responses.CRE_ORDR_UNAUTH["success"]

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, api_client: ApiClient, registered_user):
        login_resp = api_client.login(registered_user["email"], registered_user["password"])
        order_resp = api_client.create_order([], authorized=True)
        body = order_resp.json()
        assert order_resp.status_code == Responses.CRE_ORDR_NONEINGR_AUTH["code"] and \
            body.get("message") == Responses.CRE_ORDR_NONEINGR_AUTH["message"] and \
            body.get("success") is Responses.CRE_ORDR_NONEINGR_AUTH["success"]

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_invalid_ingredient_hash(self, api_client: ApiClient, registered_user):
        login_resp = api_client.login(registered_user["email"], registered_user["password"])
        bad_hashes = [invalid_ingredient_hash()]
        resp = api_client.create_order(bad_hashes, authorized=True)
        assert resp.status_code == Responses.CRE_ORDR_WRONGINGR_AUTH["code"]
