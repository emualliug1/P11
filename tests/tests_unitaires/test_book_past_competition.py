from utils import load_competitions, load_clubs


class TestBookPlaces:
    def setup_method(self):
        self.competitions = load_competitions()
        self.clubs = load_clubs()

    def test_book_closed_competition(self, client):
        result = client.get(
            f"/book/{self.competitions[0]['name']}/{self.clubs[0]['name']}"
        )
        assert result.status_code == 200

    def test_book_open_competition(self, client):
        result = client.get(
            f"/book/{self.competitions[3]['name']}/{self.clubs[0]['name']}"
        )
        assert result.status_code == 200
