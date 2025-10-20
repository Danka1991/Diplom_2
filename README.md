# Stellar Burgers API Tests

This repository contains pytest + requests + Allure tests for the Stellar Burgers API.

## Setup

```bash
pip install -r requirements.txt
```

## Run tests

```bash
pytest
```

## Generate Allure report

```bash
# Run tests and collect results (already configured via pytest.ini)
pytest

# Serve the report
allure serve allure-results
```

## Base URLs
- Web: https://stellarburgers.education-services.ru/
- API: https://stellarburgers.nomoreparties.site/