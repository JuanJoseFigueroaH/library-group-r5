from uvicorn import run
from src.app import app

if __name__ == '__main__':
    host = "0.0.0.0"
    port = 3000
    log_level = "info"
    workers = 8

    print(f"""
    @host= {host}
    @port= {port}
    @workers= {workers}
    @log_level= {log_level}
    """)
    
    run(
        "main:app", 
        host=host, 
        port=port, 
        log_level=log_level, 
        reload=True, 
        workers=workers
    )