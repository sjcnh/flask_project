#encoding: utf-8

#专门用来写命令

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from syqa import  app  # Manage初始化需要用来app，所以需要从syqa引入app
from exts import db
from models import User, Question, Answer
# 后面需要进行迁移的模型还需要导入进来

manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
