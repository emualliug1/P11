from utils import load_competitions, load_clubs


class TestLoginAndReservedPlaces:
    def setup_method(self):
        self.competitions = load_competitions()
        self.clubs = load_clubs()

    def test_login_and_reserve(self, client):
        credential = {'email': self.clubs[0]['email']}
        response = client.post('/show_summary', data=credential)

        assert response.status_code == 200





