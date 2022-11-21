import uvicorn
from app.core.config import Settings

global_settings = Settings()

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app",
        host=global_settings.host,
        log_level=global_settings.log_level,
        reload=bool(global_settings.reload),
    )
