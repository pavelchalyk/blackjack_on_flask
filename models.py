from sqlalchemy import Column, String, Integer
from database import Base


class UserHand(Base):
    __tablename__ = 'user_hand'
    id = Column(Integer, primary_key=True)
    card = Column(String)

    def __init__(self, card):
        self.card = card

    def __repr__(self):
        return self.card

class ComputerHand(Base):
    __tablename__ = 'computer_hand'
    id = Column(Integer, primary_key=True)
    card = Column(String)

    def __init__(self, card):
        self.card = card

    def __repr__(self):
        return self.card

class Deck(Base):
    __tablename__ = 'deck'
    id = Column(Integer, primary_key=True)
    card = Column(String)

    def __init__(self, card):
        self.card = card

    def __repr__(self):
        return self.card