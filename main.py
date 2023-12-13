from uvicorn import run
from src.app import app

if __name__ == '__main__':
    host = app.container.config.get("deployment")["host"]
    port = app.container.config.get("deployment")["port"] 
    log_level = app.container.config.get("deployment")["log_level"] 
    workers = app.container.config.get("deployment")["workers"]

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