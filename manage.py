#!venv/bin/python
#-*- coding: utf-8 -*-

import os

from flask_migrate import MigrateCommand
from flask_script import Manager
from app import create_app

app = create_app(os.getenv('BLOG_CONFIG') or 'default')

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
   manager.run()
