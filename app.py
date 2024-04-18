from solanacoins import app, db
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from solanacoins.models import User, SolanaCoin
from solanacoins.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/getcoin')
def index():
    coins = SolanaCoin.query.all()
    return render_template('welkom.html', coins=coins)

@app.route('/add_coin', methods=['POST'])
def add_coin():
    ticker = request.form['ticker']
    name = request.form['name']
    current_price = float(request.form['current_price'])
    current_market_cap = float(request.form['current_market_cap'])
    reason = request.form['reason']

    new_coin = SolanaCoin(ticker=ticker, name=name, current_price=current_price, current_market_cap=current_market_cap, reason=reason)
    db.session.add(new_coin)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_coin/<int:coin_id>', methods=['POST'])
def delete_coin(coin_id):
    coin = SolanaCoin.query.get_or_404(coin_id)
    db.session.delete(coin)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/welkom')
@login_required
def welkom():
    return render_template('welkom.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
          

            login_user(user)
            flash('Logged in successfully.')

       
            next = request.args.get('next')

         
            if next == None or not next[0] == '/':
                next = url_for('welkom')

            return redirect(next)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Dank voor de registratie. Er kan nu ingelogd worden!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)