"""Main module for run FastAPI application"""

import uvicorn

from src.app import app

if __name__ == '__main__':
    settings = app.state.settings

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        log_config=None,
    )
