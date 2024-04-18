from solanacoins import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# De user_loader decorator zorgt voor de flask-login voor de huidige gebruiker
# en haalt zijn/haar id op.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class SolanaCoin(db.Model):
    __tablename__ = 'solana_coins'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(6), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    current_market_cap = db.Column(db.Float, nullable=False)
    reason = db.Column(db.Text)

    def __init__(self, ticker, name, current_price, current_market_cap, reason):
        self.ticker = ticker
        self.name = name
        self.current_price = current_price
        self.current_market_cap = current_market_cap
        self.reason = reason


db.create_all()
