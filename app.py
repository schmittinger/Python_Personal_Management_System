from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
# from flaskwebgui import FlaskUI

app = Flask(__name__)
app.secret_key = "11139741"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root''@localhost/crmsys'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
# ui = FlaskUI(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200))
    lastname = db.Column(db.String(200))
    adress = db.Column(db.String(200))
    city = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(200))

    def __init__(self, firstname, lastname, adress, city, email, phone):
        self.firstname = firstname
        self.lastname = lastname
        self.adress = adress
        self.city = city
        self.email = email
        self.phone = phone


@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template('index.html', employees=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        adress = request.form['adress']
        city = request.form['city']
        email = request.form['email']
        phone = request.form['phone']

        myData = Data(firstname, lastname, adress, city, email, phone)
        db.session.add(myData)
        db.session.commit()
        flash("Daten wurden erfolgreich gespeichert")
        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.firstname = request.form['firstname']
        my_data.lastname = request.form['lastname']
        my_data.adress = request.form['adress']
        my_data.city = request.form['city']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash('Daten wurden erfolgreich geändert')
        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash('Datensatz wurde erfolgreich gelöscht')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = False
    app.run(port=5002)
