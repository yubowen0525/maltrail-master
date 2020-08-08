import sys

from Project import creat_app

# sys.path.append('./')

app = creat_app('addJob')

if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", port=25000)
    except:
        pass
