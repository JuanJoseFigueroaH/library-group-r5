from uvicorn import run
from src.app import app

if __name__ == '__main__':
    run("main:app", host="127.0.0.0", port=5000, log_level="info", reload=True)