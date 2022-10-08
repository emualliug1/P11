# -*- coding:Utf8 -*-
#############################################
# Programme Flask type
# Auteur: G.T,Nt,2022
#############################################
# Importation de fonction externe :
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for)
from essential import (
    load_clubs,
    load_competitions,
    sorted_old_competitions,
    sorted_new_competitions,
    start_places_reserved,
    update_places_reserved)
from datetime import datetime
#############################################
# Définition des constantes
MAX_BOOKED_PLACES = 12
#############################################
# Création de l'application


def create_app():
    app = Flask(__name__)
    app.secret_key = 'something_special'

    competitions = load_competitions()
    clubs = load_clubs()
    new_competitions = sorted_new_competitions(competitions)
    old_competitions = sorted_old_competitions(competitions)
    places_reserved = start_places_reserved(competitions, clubs)

    @app.route('/')
    def index():
        return render_template('index.html', clubs=clubs)

    @app.route('/show_summary', methods=['POST'])
    def show_summary():
        if request.method == 'POST':
            try:
                club = [club for club in clubs if club['email'] == request.form['email']][0]
                return render_template('welcome.html',
                                       club=club,
                                       new_competitions=new_competitions,
                                       old_competitions=old_competitions)
            except IndexError:
                if request.form['email'] == '':
                    flash('Veuillez rentrer une adresse mail.', 'error')
                else:
                    flash("Impossible de vous authentifier adresse mail inconnu.", 'error')
                return render_template('index.html')

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        found_club = [regional_club for regional_club in clubs
                      if regional_club['name'] == club][0]
        try:
            found_competition = [regional_competition for regional_competition in competitions
                                 if regional_competition['name'] == competition][0]

            if datetime.strptime(found_competition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
                flash("la competitions est terminé", 'error')

            else:
                return render_template('booking.html',
                                       club=found_club,
                                       competition=found_competition)
        except IndexError:
            flash("Il y a un problème", 'error')

        return render_template('welcome.html', club=found_club,
                               new_competitions=new_competitions,
                               old_competitions=old_competitions)

    @app.route('/purchase_places', methods=['POST'])
    def purchase_places():
        competition = [regional_competition for regional_competition in competitions
                       if regional_competition['name'] == request.form['competition']][0]
        club = [regional_club for regional_club in clubs
                if regional_club['name'] == request.form['club']][0]
        if request.method == 'POST':
            try:
                places_required = int(request.form['places'])
                if places_required > int(competition['numberOfPlaces']):
                    flash(f"Cette compétition dispose de {int(competition['numberOfPlaces'])}"
                          f" places vous ne pouvez donc pas réservé {places_required} places.", 'error')
                elif places_required > int(club['points']):
                    flash(f"Votre club dispose de {int(club['points'])}"
                          f" points vous ne pouvez donc pas réservé {places_required} places.", 'error')
                elif places_required > MAX_BOOKED_PLACES:
                    flash(f"Vous ne pouvez pas réservé plus de {MAX_BOOKED_PLACES} places par compétitions.", 'error')
                else:
                    try:
                        update_places_reserved(competition, club, places_reserved, places_required)
                        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
                        club['points'] = int(club['points']) - places_required
                        flash(f'Vous avez réservé {places_required} places.', 'success')

                        return render_template('welcome.html',
                                               club=club,
                                               new_competitions=new_competitions,
                                               old_competitions=old_competitions)

                    except ValueError as first_error:
                        flash(f"{first_error}", 'error')

            except ValueError:
                flash(f'Veuillez saisir une valeur numérique comprise entre 1 et 12', 'error')

            return render_template('booking.html',
                                   club=club,
                                   competition=competition)

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    @app.route('/tableau_points')
    def tableau_points():
        sorted_clubs = sorted(clubs, key=lambda club: int(club['points']), reverse=True)
        return render_template('tableau_points.html', clubs=sorted_clubs)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
