echo "[0/2] venv activation..."
call app\venv\Scripts\activate

echo "[1/2] Run docker-compose..."
docker-compose up -d

echo "[2/2] Run GUI-app..."
python app/main.py