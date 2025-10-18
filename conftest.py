import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import pytest
import allure

from src.api.api_client import ApiClient
from helper import random_email, random_password

@pytest.fixture(scope="session")
def api_client():
    return ApiClient()

@pytest.fixture()
@allure.step("Generate unique user credentials")
def new_user_creds():
    email = random_email("yandex.ru")
    password = random_password()
    name = "QA User"
    return {"email": email, "password": password, "name": name}

@pytest.fixture()
@allure.step("Create a registered user")
def registered_user(api_client: ApiClient, new_user_creds):
    resp = api_client.register(new_user_creds)
    i = 0 
    while resp.status_code != 201 and i <= 5: # иногда генерируется логин который уже зарегистрирован в системе, поэтому если регистраци не удалась, пробуем еще
        new_user_creds = {"email": random_email("yandex.ru"), "password": random_password(), "name": "QA User"}
        resp = api_client.register(new_user_creds)
        i += 1
    return new_user_creds
