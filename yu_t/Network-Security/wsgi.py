from Project import creat_app
from Project.extension import db

app = creat_app('testing')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
