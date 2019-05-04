from flask import Flask, render_template_string, redirect, url_for
from sqlalchemy import create_engine, MetaData
from flask_login import UserMixin, LoginManager, login_user, logout_user
from flask_blogging import SQLAStorage, BloggingEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'humansLeSuck'
app.config['BLOGGING_URL_PREFIX'] = '/'
app.config['BLOGGING_SITENAME'] = 'Anti-Human League Blog'


# extensions
engine = create_engine('sqlite:///blog.db')
meta = MetaData()
sql_storage = SQLAStorage(engine, metadata=meta)
blog_engine = BloggingEngine(app, sql_storage)
login_manager = LoginManager(app)
meta.create_all(bind=engine)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    def get_name(self):
        return 'Paul Dirac'  # typically the user's name

@login_manager.user_loader
@blog_engine.user_loader
def load_user(user_id):
    return User(user_id)

@app.cli.command('initdb')
def initdb_command():
    pass  # I think just executing this file will create the db

if __name__ == '__main__':
    app.run(debug=True, port=8000, use_reloader=True)
