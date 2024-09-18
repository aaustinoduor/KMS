import os
from waitress import serve
from key_manager import create_app
from key_manager.config import Env, DevConfig, ProdConfig


# Set configurations based of the environment the application is running
# that is either
if os.getenv("FLASK_ENV") == Env.PROD:
    app = create_app(ProdConfig())
else:
    app = create_app(DevConfig())

if __name__ == '__main__':
    # serve(app, host=app.config.get("HOST"), port=app.config.get("PORT"))
    app.run(host=app.config.get("HOST"), debug=app.config.get("DEBUG"),
            port=app.config.get("PORT"))
