from __future__ import annotations

import random
import string

def random_email(domain = "example.com"):
    prefix = "qa_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{prefix}@{domain}"

def random_password(min_len = 8, max_len = 12):
    length = random.randint(min_len, max_len)
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choices(alphabet, k=length))

def valid_ingredient_hashes(ingredients_response_json, limit = 2):
    data = ingredients_response_json.get("data") or ingredients_response_json.get("ingredients") or []
    ids = [item.get("_id") for item in data if item.get("_id")]
    return ids[:limit]

def invalid_ingredient_hash():
    return "11dff41ab44cab0026agggc6"
