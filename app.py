from flask import Flask, sessions
from flask_login import LoginManager, UserMixin, current_user, LoginManager, UserMixin, login_user
from database import db, Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'login'
@app.route('/')
def home():  # put application's code here
    return 'Hello World!'


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
