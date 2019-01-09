from app import my_app

run_app = my_app('development')

if __name__ == '__main__':
    run_app.run(port=8000)
