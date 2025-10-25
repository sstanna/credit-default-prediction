# Credit Default Prediction Pipeline  
Автоматизированный ML-конвейер для прогнозирования дефолта по кредитам (PD-модель)

## Описание проекта

Этот проект реализует сквозной автоматизированный конвейер для разработки, тестирования, деплоя и мониторинга моделей машинного обучения, предназначенных для прогнозирования вероятности дефолта клиента.

**Область применения:** Финансы / Кредитный скоринг  
**Источник данных:** Default of Credit Card Clients Dataset (UCI Machine Learning Repository)

---

## Структура проекта

```
credit-default-prediction/
├── data/                   # Данные (сырые, обработанные)
├── models/                 # Обученные модели
├── notebooks/              # Jupyter-ноутбуки для EDA
├── src/                    # Исходный код
│   ├── data/               # Модули обработки данных
│   ├── models/             # Модули обучения моделей
│   ├── api/                # Приложение FastAPI
│   └── monitoring/         # Модули мониторинга
├── tests/                  # Тесты
├── scripts/                # Скрипты запуска
├── .github/workflows/      # GitHub Actions (CI/CD)
├── dvc.yaml                # DVC-конвейер
├── Dockerfile              # Конфигурация Docker
└── requirements.txt        # Зависимости
```

---

## Установка и настройка

### 1. Клонирование репозитория
```bash
git clone https://github.com/sstanna/credit-default-prediction.git
cd credit-default-prediction
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Подготовка данных
```bash
python -m src.data.load_data
```

### 4. Обучение модели
```bash
python scripts/train_models.py
```

### 5. Запуск API
```bash
python scripts/run_api.py
# или
uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

### 6. Запуск тестов
```bash
pytest tests/ -v
```

### 7. Мониторинг дрейфа данных
```bash
python scripts/monitor_drift.py
```

### 8. Запуск через Docker
```bash
docker build -t credit-default-api .
docker run -p 8000:8000 credit-default-api
```

---

## Компоненты проекта

### 1. Подготовка и валидация данных
- Загрузка данных с UCI Repository  
- Генерация и агрегирование признаков  
- Валидация данных с помощью Great Expectations

### 2. Обучение модели
- Использование Sklearn Pipeline  
- Автоматический подбор гиперпараметров  
- Метрики: ROC-AUC, Precision, Recall, F1-Score

### 3. Эксперименты и трекинг
- Логирование экспериментов через MLflow  
- Версионирование данных и моделей с DVC

### 4. Тестирование и CI/CD
- Юнит-тесты через pytest  
- Автоматизация тестов с GitHub Actions  
- Линтинг и форматирование с помощью flake8 и black

### 5. Развёртывание и мониторинг
- REST API на FastAPI  
- Контейнеризация в Docker  
- Мониторинг дрейфа данных через PSI

---

## API Эндпоинты

| Метод | Эндпоинт | Описание |
|-------|-----------|-----------|
| GET | / | Информация об API |
| POST | /predict | Прогноз вероятности дефолта |
| GET | /health | Проверка статуса API |
| POST | /predict_batch | Пакетное предсказание |
| GET | /model_info | Информация о модели |

---

## Пример использования API

```python
import requests

url = "http://localhost:8000/predict"
data = {
    "LIMIT_BAL": 20000,
    "SEX": 2,
    "EDUCATION": 2,
    "MARRIAGE": 1,
    "AGE": 24,
    "PAY_0": 2,
    "PAY_2": 2,
    "PAY_3": -1,
    "PAY_4": -1,
    "PAY_5": -2,
    "PAY_6": -2,
    "BILL_AMT1": 3913,
    "BILL_AMT2": 3102,
    "BILL_AMT3": 689,
    "BILL_AMT4": 0,
    "BILL_AMT5": 0,
    "BILL_AMT6": 0,
    "PAY_AMT1": 0,
    "PAY_AMT2": 689,
    "PAY_AMT3": 0,
    "PAY_AMT4": 0,
    "PAY_AMT5": 0,
    "PAY_AMT6": 0
}

response = requests.post(url, json=data)
print(response.json())
```

---

## Мониторинг дрейфа данных

```python
from src.monitoring.drift_monitor import DataDriftMonitor

monitor = DataDriftMonitor(reference_data)
report = monitor.generate_drift_report(new_data)
```

---

## MLflow Трекинг

Запуск интерфейса MLflow:
```bash
mlflow ui
```

Откройте http://localhost:5000 для просмотра экспериментов.

---

## DVC Pipeline

Запуск всего конвейера:
```bash
dvc repro
```

---

## Тестирование и проверка качества

```bash
pytest tests/ -v --cov=src
flake8 src tests
black src tests
```

---

## Результаты

- Обработано записей: 30,000  
- Доля дефолтов: 22.12% (6,636 клиентов)  
- Создано признаков: 4 новых  
- Обучено моделей: 3 с оптимизацией гиперпараметров  
- API: Готово к продакшену  
- Мониторинг: Реализован PSI-дрейф детектор

