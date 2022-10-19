"""Main entrypoint for container startup."""
from iris_api.config import app_cfg
from iris_api.main import app

import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=app_cfg.app.host,
        port=app_cfg.app.port,  # log_level=app_cfg.log.level
    )
