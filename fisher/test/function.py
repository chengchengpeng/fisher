from flask import Flask
app = Flask(__name__)
from  flask import request
class A:
    c = 1


n = A()


@app.route('/test1')
def hello_world():
    print(n.c)
    n.c = 2

    print(getattr(request, 'v', None))
    getattr(request, 'v', 2)
    print('--------------------')
    return 'Hello World T1122221!'


if __name__ == '__main__':
    app.run('0.0.0.0', port=81, debug=True)