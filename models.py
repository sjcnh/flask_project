#encoding: utf-8

#专门用来写模型
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    telephone = db.Column(db.String(11), nullable= False)
    username = db.Column(db.String(50), nullable= False)
    pwd = db.Column(db.String(100), nullable= False)

    def __init__(self, *args, **kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('pwd') #这个是从syqa User 获取的
        self.telephone = telephone
        self.username = username
        self.pwd = generate_password_hash(password)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    title = db.Column(db.String(100), nullable= False)
    content = db.Column(db.Text, nullable= False)
    # now()获取的是服务器第一次运行的时间
    # now 就是每次创建一个模型的时候，都获取当前的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref = db.backref('questions'))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    content = db.Column(db.Text, nullable= False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)


    # 模型中不能使用syqa中的-create_time方式进行倒叙，只能采用 .desc()方法！
    # eg： question = db.relationship('Question', backref = db.backref('answers', order_by = id.desc()))
    # 最好是根据时间倒叙
    question = db.relationship('Question', backref = db.backref('answers', order_by = create_time.desc()))
    author = db.relationship('User', backref = db.backref('answers'))
    # 由这个外键查询到的这个问题，或者这个作者的所有回答

