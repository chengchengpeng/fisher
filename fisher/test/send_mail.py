# # -*- coding: utf-8 -*-
from flask import Flask, request
from flask_script import Manager, Shell
from flask_mail import Mail, Message, current_app
import time
from threading import Thread
import os

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '2946530796@qq.com'
app.config['MAIL_PASSWORD'] = 'bxdgintbqqioddbj'
mail = Mail(app)

def send_mail(msg):
    with app.app_context():
        mail.send(msg)
@app.route('/test')
def hello():

    msg = Message('标题', sender='2946530796@qq.com', recipients=['2946530796@qq.com'])
    msg.body = '内容'
    new_t = Thread(target=send_mail, args=[msg])
    new_t.start()
    # time.sleep(10)
    # with app.app_context():
    #     mail.send(msg)
    return '1221'


if __name__ == '__main__':
    app.run('0.0.0.0', port=81, debug=True)
