import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    SQL_DATABASE_URI = 'sqlite:///database.db'
    SQLAlchemy_TRACK_Modify = False

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    wallet = db.Column(db.Integer, nullable=False, default=0.0)
    wins = db.Column(db.Integer, nullable=False, default=0)
    losses = db.Column(db.Integer, nullable=False, default=0)
    transactions = db.Column(db.Integer, nullable=False, default=0)

class Bets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    odds = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False) #parlay, sgp, straight


class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)



