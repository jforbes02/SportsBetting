from database import *
from app import *


def make_bet(user_id, amount):
    """
    When react selects the submit button I want this to process it
    It will input the wager amount,
    """
    user = session.query(User).filter_by(id=user_id).get(current_user.id)
    if user.wallet + amount < 0:
        raise Exception('You do not have enough money for this bet')

