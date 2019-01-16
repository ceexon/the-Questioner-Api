import os
from app.app_v2 import create_app

app = create_app(os.getenv("APP_SETTINGS"))


if __name__ == '__main__':
    app.run()
