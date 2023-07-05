# Используйте официальный образ Python
FROM python:3.9

# Установите рабочую директорию для приложения
WORKDIR /app

# Копируйте файлы с зависимостями
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте исходный код приложения
COPY main.py .

# Запустите приложение
CMD ["python", "main.py"]
