from app import create_app
import os

app = create_app(os.getenv("APP_SETTINGS"))
app.config["SECRET_KEY"] = os.getenv('SECRET')


if __name__ == '__main__':
    app.run()
