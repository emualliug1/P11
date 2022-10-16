from utils import load_clubs
from utils import load_competitions


class TestLoadJson:
    def test_load_competitions(self):
        """test du chargement du fichier json competitions.json"""
        data = load_competitions()
        assert type(data) is list

    def test_load_clubs(self):
        """test du chargement du fichier json clubs.json"""
        data = load_clubs()
        assert type(data) is list


