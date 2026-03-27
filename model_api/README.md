# Churn Prediction API

API для предсказания статуса клиента: ушел, остался или присоединился.

## Модель

- Алгоритм: Decision Tree Classifier
- Целевая переменная: Customer Status (Churned, Stayed, Joined)
- Признаки: 37 features (демография, услуги, биллинг)

## Эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/predict` | Предсказание статуса клиента |
| GET | `/docs` | Swagger документация |

## Пример запроса

```json
{
  "customer_id": "CUST001",
  "gender": "Female",
  "age": 45,
  "married": "Yes",
  "number_of_dependents": 2,
  "city": "Los Angeles",
  "zip_code": 90001,
  "latitude": 34.0522,
  "longitude": -118.2437,
  "number_of_referrals": 3,
  "tenure_in_months": 36,
  "offer": "Offer A",
  "phone_service": "Yes",
  "avg_monthly_long_distance_charges": 15.5,
  "multiple_lines": "No",
  "internet_service": "Yes",
  "internet_type": "Fiber Optic",
  "avg_monthly_gb_download": 150.5,
  "online_security": "Yes",
  "online_backup": "No",
  "device_protection_plan": "Yes",
  "premium_tech_support": "No",
  "streaming_tv": "Yes",
  "streaming_movies": "Yes",
  "streaming_music": "No",
  "unlimited_data": "Yes",
  "contract": "Month-to-Month",
  "paperless_billing": "Yes",
  "payment_method": "Credit Card",
  "monthly_charge": 89.99,
  "total_charges": 2159.76,
  "total_refunds": 0,
  "total_extra_data_charges": 0,
  "total_long_distance_charges": 45.2,
  "total_revenue": 2204.96
}
```

## Пример ответа

```json
{
  "class_ind": 2
}
```

### Классы
- `0` — Churned (ушел)
- `1` — Stayed (остался)
- `2` — Joined (присоединился)

## Локальный запуск

```bash
cd model_api
pip install -r requirements.txt
uvicorn app:app --reload
```

## Деплой

Развернуто на Render.