from flask import Flask
from flask import render_template
import random
from database import db_session, init_db
from models import Deck, UserHand, ComputerHand

app = Flask(__name__)

CARD_SCORES = {
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'Valet': 2,
    'Dama': 3,
    'Korol': 4,
    'Tuz': 11
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/start_game')
def start_game():
    init_or_flush_cards()
    generate_deck()
    i = 0
    while i < 2:  # Both gamers get 2 cards from deck to start the game
        add_user_card(get_card_from_deck())
        add_computer_card(get_card_from_deck())
        i += 1
    user_cards = get_user_cards()
    return render_template('game.jinja2', user_cards=user_cards, user_score=calc_score(user_cards))


@app.route('/get_card')
def get_card():
    add_user_card(get_card_from_deck())
    computer_score = calc_score(get_computer_cards())
    if computer_score < 17 or (21 - computer_score > 2):  # Computer should get card in case of it's score < 17
        add_computer_card(get_card_from_deck())
    user_cards = get_user_cards()
    return render_template('game.jinja2', user_cards=user_cards, user_score=calc_score(user_cards))


@app.route('/stop')
def stop():
    user_score = calc_score(get_user_cards())
    computer_score = calc_score(get_computer_cards())
    if (user_score > 21 and computer_score > 21) or user_score == computer_score:
        result = 'Friendship won'
    elif user_score <= 21 and computer_score > 21:
        result = 'You won'
    elif user_score > 21 and computer_score <= 21:
        result = 'You lose'
    elif user_score > computer_score:
        result = 'You won'
    else:
        result = 'You lose'
    return render_template('score.jinja2', result=result, computer_score=computer_score, user_score=user_score)


def init_or_flush_cards():
    '''
    Creates tables and clears them
    '''
    init_db()
    for database in [UserHand, ComputerHand, Deck]:
        database.query.delete()
    save()


def generate_deck():
    '''
    Generates list of cards and stores it to model
    '''
    deck = [a for a in CARD_SCORES.keys()] * 4
    random.shuffle(deck, random.random)
    for card in deck:
        card = Deck(str(card))
        db_session.add(card)
    save()


def get_deck():
    return Deck.query.all()


def get_user_cards():
    return UserHand.query.all()


def get_computer_cards():
    return ComputerHand.query.all()


def add_user_card(card):
    card = UserHand(card)
    db_session.add(card)
    save()


def add_computer_card(card):
    card = ComputerHand(card)
    db_session.add(card)
    save()


def get_card_from_deck():
    '''
    Gets top card and removes it from deck
    :return: card String
    '''
    deck = get_deck()
    card = str(deck.pop(0))
    db_session.delete(Deck.query.filter_by(card=card).first())
    save()
    return card


def save():
    try:
        db_session.commit()
    except Exception as e:
        print e


def calc_score(cards):
    '''
    :param cards: List of cards
    :return: Score of given cards set
    '''
    score = 0
    for card in cards:
        score += CARD_SCORES[str(card)]
    return score


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    print exception


if __name__ == '__main__':
    app.run()
