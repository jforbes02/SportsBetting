from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Coolpyro55@localhost:5432/sportsbetting'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    wallet = db.Column(db.Integer, nullable=False, default=0.0)
    wins = db.Column(db.Integer, nullable=False, default=0)
    losses = db.Column(db.Integer, nullable=False, default=0)
    transactions = db.Column(db.Integer, nullable=False, default=0)
    bets = db.relationship('Bet', backref='user', lazy='select')
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def remove(self):
        db.session.delete(self)

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    number = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(15), nullable=False)
    season = db.Column(db.String(10), nullable=False)
    avgPoints = db.Column(db.Numeric(4, 1), nullable=False)
    avgRebounds = db.Column(db.Numeric(4, 1), nullable=False)
    avgAssists = db.Column(db.Numeric(4, 1), nullable=False)
    avgSteals = db.Column(db.Numeric(3, 1), nullable=False)
    avgBlocks = db.Column(db.Numeric(3, 1), nullable=False)
    avgTurnovers = db.Column(db.Numeric(3, 1), nullable=False)
    fgPercentage = db.Column(db.Numeric(3, 1), nullable=False)

    team = db.relationship('Teams', backref='players')
    def __repr__(self):
        return f'<Player {self.name} ({self.team.inShort})>'

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    inShort = db.Column(db.String(4), nullable=False, unique=True)
    location = db.Column(db.String(25), nullable=False)
    wins = db.Column(db.Integer, nullable=False, default=0)
    losses = db.Column(db.Integer, nullable=False, default=0)

    players = db.relationship('Players', backref='teams')
    def __repr__(self):
        return f'<Team {self.inShort}>'


class Bet(db.Model):
    __tablename__ = 'bets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False) #SGP, Straights, Legs etc
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    odds = db.Column(db.Numeric(6, 1), nullable=False)

    def __repr__(self):
        return f'<Bet {self.id} by {self.user.username}>'
