echo "[0/2] Активація віртуального середовища..."
call app\venv\Scripts\activate

echo "[1/2] Запуск docker-compose..."
docker-compose up -d

echo "[2/2] Запуск GUI-додатку..."
python app/main.py