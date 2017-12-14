#encoding: utf-8
from flask import session, redirect, url_for
from functools import wraps
# 登录限制的装饰器
def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
            # 为什么要写return，因为不写无法返回这个func()
        else:
            return redirect(url_for('login'))
    return wrapper
