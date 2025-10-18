import allure
import pytest

from src.api.api_client import ApiClient
from responses import Responses

class TestUserLogin:
    @allure.title('Создание уникального пользователя')
    def test_register_unique_user(self, api_client: ApiClient, new_user_creds):
        resp = api_client.register(new_user_creds)
        body = resp.json()
        assert resp.status_code == Responses.REG_UNIQUE_USER["code"] and \
            body.get("user", {}).get("email") == new_user_creds["email"] and \
            body.get("success") is Responses.REG_UNIQUE_USER["success"] 

    @allure.title('Создание пользователя, который уже зарегистрирован')
    def test_register_duplicate_user(self, api_client: ApiClient, registered_user):
        resp = api_client.register(registered_user)
        body = resp.json()
        assert resp.status_code == Responses.REG_DUPLICATE_USER["code"] and \
            body.get("message") == Responses.REG_DUPLICATE_USER["message"] and \
            body.get("success") is Responses.REG_DUPLICATE_USER["success"]

    @allure.title('Создание пользователя, без одного из обязательных полей')
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_register_missing_field(self, api_client: ApiClient, new_user_creds, missing_field):
        payload = dict(new_user_creds)
        payload.pop(missing_field)
        resp = api_client.register(payload)
        body = resp.json()
        assert resp.status_code == Responses.REG_USER_MISSING_FIELD["code"] and \
            body.get("message") == Responses.REG_USER_MISSING_FIELD["message"] and \
            body.get("success") is Responses.REG_DUPLICATE_USER["success"]
 
    @allure.title('Вход под существующим пользователем')
    def test_login_existing_user(self, api_client: ApiClient, registered_user):
        resp = api_client.login(registered_user["email"], registered_user["password"])
        body = resp.json()
        assert resp.status_code == Responses.LOG_EXIST_USER["code"] and \
            isinstance(body.get("accessToken"), str) and \
            body.get("success") is Responses.LOG_EXIST_USER["success"]

    @allure.title('Вход с неверным логином и паролем, пользователь зарегистрирован в системе')
    def test_login_invalid_credentials(self, api_client: ApiClient, registered_user):
        resp = api_client.login(registered_user["email"], "memyselfandithinkthisisawrongpass")
        body = resp.json()
        assert resp.status_code == Responses.LOG_USER_INVAL_CREDS["code"] and \
            body.get("message") == Responses.LOG_USER_INVAL_CREDS["message"] and \
            body.get("success") is Responses.LOG_USER_INVAL_CREDS["success"]

