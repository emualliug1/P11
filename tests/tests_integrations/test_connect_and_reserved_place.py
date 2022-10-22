from utils import load_competitions, load_clubs


class TestLoginAndReservedPlaces:
    def setup_method(self):
        self.competitions = load_competitions()
        self.clubs = load_clubs()

    def test_login_and_reserve(self, client):
        credential = {'email': self.clubs[3]['email']}
        client.post('/show_summary', data=credential)
        response = client.post('/purchase_places',
                    data={"competition": self.competitions[3]['name'],
                          "club": self.clubs[3]['name'],
                          "places": 2})
        expected_points = '498'
        assert response.status_code == 200
        data = response.data.decode()
        assert expected_points in data




