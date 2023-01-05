import uvicorn
from app.core.config import Settings

global_settings = Settings()

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app",
        host=global_settings.host,
        port=global_settings.port,
        log_level=global_settings.log_level,
        reload=bool(global_settings.reload),
    )
