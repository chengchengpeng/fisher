# 代理对象去查找flask的核心对象，是通过线程的id号去查找的，代理对象是受到线程id的影响的，因为他本身就是在做线程隔离
from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_async_email(app, msg):
    with app.qpp_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass



def send_mail(to, subject, template, **kwargs):
    msg = Message('[鱼书]' + '' + subject,
                  sender=current_app.config['MAIL_USENAME'],
                  recipients=[to])
    # 使邮件返回一段html
    msg.html = render_template(template, **kwargs)
    # 这个方法可以拿到flask真正的核心对象app
    app = current_app._get_current_object()
    thr = Thread(target = send_async_email, args=[app, msg])
    thr.start()
    mail.send(msg)
