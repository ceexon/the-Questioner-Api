from app import my_app

my_app.config["FLASK_ENV"] = "development"

if __name__ == '__main__':
    my_app.run(port=8080, debug=True)
