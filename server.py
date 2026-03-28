import json
from flask import Flask, render_template, request, redirect, flash, url_for, session

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if (email == "admin" and password == "admin") or (email in ("admin@admin.com", "admin@admin") and password == "root"):
            session['is_admin'] = True
            return redirect(url_for('welcomeAdmin'))

        return "<h3>Unauthorized</h3><p><a href='/admin'>Back to login</a></p>"

    return render_template('admin.html')


@app.route('/welcomeAdmin')
def welcomeAdmin():
    return render_template('welcomeAdmin.html')


@app.route('/welcome')
def welcome():
    if 'email' not in session:
        return "Please enter your secretary email"

    club = next((c for c in clubs if c['email'] == session['email']), None)
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form.get('email')

    if not email:
        return "Please enter your secretary email"

    result = [club for club in clubs if club['email'] == email]
    if not result:
        return "Unauthorized", 401

    club = result[0]

    session['email'] = email

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)

    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong - please try again")
        return render_template('welcome.html', competitions=competitions)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    placesRequired = int(request.form['places'])

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    flash('Great - booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, send_file
import subprocess

@app.route("/runTests")
def runTests():
    subprocess.call(["pytest", "--html=report.html", "--self-contained-html", "-q"])
    return "Tests executed! <a href='/report'>Voir le rapport</a>"

@app.route("/report")
def showReport():
    return send_file("report.html")
@app.route("/reportViewer")
def reportViewer():
    return render_template("reportViewer.html")