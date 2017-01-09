#!venv/bin/python
#-*- coding: utf-8 -*-

import os
from app import create_app, db, models
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flaskext.markdown import Markdown

app = create_app(os.getenv('BLOG_CONFIG') or 'default')


@app.context_processor
def subject_processor():
    subjects = models.Subject.query.all()
    return dict(subjects=subjects)

manager = Manager(app)
migrate = Migrate(app, db, render_as_batch=True)
markdown = Markdown(app)


# 添加命令shell， 导入这些变量到shell环境
def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
   manager.run()
