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
    #registration
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    #account info
    wallet = db.Column(db.Integer, nullable=False, default=0.0)

    def update_wallet(self, amount):
        self.wallet += amount
        return self.wallet

    wins = db.Column(db.Integer, nullable=False, default=0)
    losses = db.Column(db.Integer, nullable=False, default=0)
    transactions = db.Column(db.Integer, nullable=False, default=0)
    bets = db.relationship('Bet', backref='user', lazy='select')

    #passwording (werkzeug)
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

    #personal
    name = db.Column(db.String(80), nullable=False)
    number = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(15), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    college = db.Column(db.String(80), nullable=False) #college, g league unite, overseas etc
    birthdate = db.Column(db.Date)
    season = db.Column(db.String(10), nullable=False)

    #stats
    games_played = db.Column(db.Integer, nullable=False) # games played current season
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
    conference = db.Column(db.String(20), nullable=False)

    players = db.relationship('Players', backref='teams', lazy='select')
    home_games = db.relationship('Game', foreign_keys='Game.home_team_id', backref='home_team', lazy='select')
    away_games = db.relationship('Game', foreign_keys='Game.away_team_id', backref='away_team', lazy='select')

    def __repr__(self):
        return f'<Team {self.inShort}>'


class Bet(db.Model):
    __tablename__ = 'bets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False) #SGP, Straights, Legs etc
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    odds = db.Column(db.Numeric(6, 1), nullable=False)
    status = db.Column(db.String(10), default="pending") # won, loss, pending, void
    money_in = db.Column(db.Float, nullable=False)
    selection = db.column(db.String(20))

    transactions = db.relationship('Transaction', backref='bet', lazy='select')
    def __repr__(self):
        return f'<Bet {self.id} by {self.user.username}>'


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    #do I want this in the database though?
    home_score = db.Column(db.Integer, nullable=False, default=0)
    away_score = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(15), nullable=False) # scheduled, live, done

    location = db.Column(db.String(50), nullable=False)
    season = db.Column(db.String(10), nullable=False)

    lines = db.relationship('bets', backref='game',lazy='select')
    player_props = db.relationship('player_props', backref='game', lazy='select')

class PlayerProp(db.Model):
    #indiviual lines for each player
    __tablename__ = 'player_props'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    prop_name = db.Column(db.String(5), nullable=False) # p, pr, pra, r, ra, a, pa

    over_odds = db.Column(db.Integer, nullable=False) # +250, -235
    under_odds = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=datetime.utcnow,default=datetime.utcnow)

    is_active = db.Column(db.Boolean, default=True)

    game = db.relationship('Game')
    bets = db.relationship('Bet', backref='player')

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    trans_type = db.Column(db.String(20), nullable=False)
    bet_id = db.Column(db.Integer, db.ForeignKey('bets.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.trans_type} ${self.amount:.2f} for user {self.user_id}>'