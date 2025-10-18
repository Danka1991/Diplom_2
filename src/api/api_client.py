from __future__ import annotations

import requests
from curl import Urls as ep

class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None

    def _auth_headers(self):
        if not self.access_token:
            return {}
        return {"Authorization": self.access_token}

    def register(self, payload):
        return self.session.post(ep.REGISTER, json=payload)

    def login(self, email, password):
        payload = {"email": email, "password": password}
        resp = self.session.post(ep.LOGIN, json=payload)
        if resp.ok:
            data = resp.json()
            self.access_token = data.get("accessToken")
        return resp

    def get_ingredients(self):
        return self.session.get(ep.INGREDIENTS)

    def create_order(self, ingredients = None, authorized = False):
        json_payload = {}
        if ingredients is not None:
            json_payload["ingredients"] = ingredients
        headers = self._auth_headers() if authorized else {}
        return self.session.post(ep.ORDERS, json=json_payload, headers=headers)