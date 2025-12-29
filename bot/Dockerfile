# 1. Базовий образ з Python
FROM python:3.12-slim

# 2. Робоча директорія всередині контейнера
WORKDIR /app

# 3. Копіюємо requirements.txt окремо (оптимізація кешу)
COPY requirements.txt .

# 4. Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копіюємо весь проєкт
COPY . .

# 6. Вказуємо Python, де шукати модулі
ENV PYTHONPATH=/app/src

# 7. Запуск CLI-застосунку
CMD ["python", "-m", "bot.main"]

