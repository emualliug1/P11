from flask import Flask, render_template, request, redirect, flash, url_for
from load_json import load_clubs, load_competitions


def create_app():
    app = Flask(__name__)
    app.secret_key = 'something_special'
    competitions = load_competitions()
    clubs = load_clubs()

    @app.route('/')
    def index():
        return render_template('index.html', clubs=clubs)

    @app.route('/show_summary', methods=['POST'])
    def show_summary():
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
        except (IndexError, KeyError):
            return page_not_found()
        return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        found_club = [c for c in clubs if c['name'] == club][0]
        found_competition = [c for c in competitions if c['name'] == competition][0]
        if found_club and found_competition:
            return render_template('booking.html', club=found_club, competition=found_competition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/purchase_places', methods=['POST'])
    def purchase_places():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        places_required = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    @app.errorhandler(404)
    def page_not_found():
        return render_template('404.html'), 404

    return app


if __name__ == '__server__':
    create_app().run()
