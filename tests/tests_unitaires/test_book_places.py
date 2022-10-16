from utils import load_competitions, load_clubs


class TestBookPlaces:
    def setup_method(self):
        self.competitions = load_competitions()
        self.clubs = load_clubs()

    def test_left_competition_places(self, client):
        booked_places = 4
        competition_places = int(self.competitions[2]['numberOfPlaces'])
        data = {
            "competition": self.competitions[2]['name'],
            "club": self.clubs[0]['name'],
            "places": booked_places,

        }
        response = client.post('/purchase_places', data=data)
        expected_competition = 'test01'
        expected_club = 'Simply Lift'
        expected_places = competition_places - booked_places
        data = response.data.decode()
        assert response.status_code == 200
        assert self.competitions[2]['name'] == expected_competition
        assert self.clubs[0]['name'] == expected_club
        assert f"Vous avez réservé {booked_places} places." in data
        assert str(expected_places) in data

    def test_left_club_points(self, client):
        booked_places = 6
        club_points = int(self.clubs[2]['points'])
        data = {
            "competition": self.competitions[3]['name'],
            "club": self.clubs[2]['name'],
            "places": booked_places
        }
        response = client.post('/purchase_places', data=data)
        expected_competition = 'test02'
        expected_club = 'She Lifts'
        expected_points = club_points - booked_places
        data = response.data.decode()
        assert response.status_code == 200
        assert self.competitions[3]['name'] == expected_competition
        assert self.clubs[2]['name'] == expected_club
        assert f"Vous avez réservé {booked_places} places." in data
        assert str(expected_points) in data

    def test_error_maximum_booked_places(self, client):
        booked_places = 13
        data = {
            "competition": self.competitions[3]['name'],
            "club": self.clubs[0]['name'],
            "places": booked_places
        }
        response = client.post('/purchase_places', data=data,)
        expected_error = 'Vous ne pouvez pas réservé plus de 12 places par compétitions.'
        data = response.data.decode()
        assert response.status_code == 200
        assert expected_error in data

    def test_error_club_have_no_enough_points(self, client):
        booked_places = 7
        data = {
            "competition": self.competitions[3]['name'],
            "club": self.clubs[1]['name'],
            "places": booked_places
        }
        response = client.post('/purchase_places',
                               data=data,
                               follow_redirects=True)
        expected_error = f"Votre club dispose de {int(self.clubs[1]['points'])} points vous ne pouvez donc pas réservé {booked_places} places."
        data = response.data.decode()
        assert response.status_code == 200
        assert expected_error in data
