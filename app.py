from flask import Flask, request, session
from flask_login import logout_user, login_required, current_user, LoginManager, login_user
from database import db, Config, User, Players, Bets

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQL_DATABASE_URI

@app.route('/')
def home():  # put application's code here
    return 'Hello World!'

@app.route('/register', methods=['GET', 'POST'])
def registration():
    return 'register'

if __name__ == '__main__':
    app.run()
