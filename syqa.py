#encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Question, Answer
from exts import db
from decorators import login_required
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app) #一定不能忘记！！


@app.route('/')
def index():
    context = {
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)

# index = login_required(index) = wrapper
# index = wrapper
# index() = wrapper()

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.pwd == password).first()
        if user:
            session['user_id'] = user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机或者密码错误，请确认后再登录！'

@app.route('/logout/')
def logout():
    session.pop('user_id')
    # del session['user_id']
    # session.clear()
# 以上方法都可以
    return redirect(url_for('login'))

@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        pwd2 = request.form.get('pwd2')
        #手机号码验证，如果被注册了，那么就不能再注册了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已被注册，请更换手机号码！'
        else:
            # pwd1要和pwd2相等才可以
            if pwd != pwd2:
                return u'两次密码不相等，请核对后再填写'
            else:
                user = User(telephone = telephone, username = username, pwd = pwd)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title = title, content = content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>', methods=['GET', 'POST'])
def detail(question_id):
    if request.method == 'GET':
        # context = {
        #     'question': Question.query.filter(Question.id == question_id).first()
        # }  这种方法也可以！
        # return render_template('detail.html', **context) 对应第一种方法
        question_model = Question.query.filter(Question.id == question_id).first()
        return render_template('detail.html', question = question_model) # 第一个question是模板中变量名称！！


@app.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
    comment = request.form.get('answer_comment')
    question_id = request.form.get('question_id')
    answer = Answer(content = comment) # 前者为模型数据库中的名称！
    user_id = session['user_id'] # 如果当前没有登录，则会报错！所以需要添加login_required装饰器！
    user = User.query.filter(User.id == user_id).first()
    question = Question.query.filter(Question.id == question_id).first()
    answer.author = user
    answer.question = question
    # 把评论/回答提交！
    db.session.add(answer)
    # 事务提交
    db.session.commit()
    # return redirect(url_for('detail'), question_id == question_id ) 括号对齐问题很重要，否则参数无法回传！
    return redirect(url_for('detail', question_id = question_id)) # 这里是通过question_id重载页面，而不是==

# ?xx=xxx 使用字符串形式，不需要写<id>
@app.route('/search/')
def search():
    q = request.args.get('q')
#   title, content
#   或 sqlAlchemy 需要导入or_
    condition = or_(Question.title.contains(q), Question.content.contains(q))
    questions = Question.query.filter(condition).order_by('-create_time')
    # 如果需要and，如下操作即可：
    # questions = Question.query.filter(Question.title.contains(q), Question.content.contains(q)).order_by('-create_time')

    return render_template('index.html', questions = questions)


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}



if __name__ == '__main__':
    app.run()
