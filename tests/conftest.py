import pytest
# -*- coding:Utf8 -*-
#############################################
# Programme Flask type
# Auteur: G.T,Nt,2022
#############################################
# Importation de fonction externe :
from server import create_app
#############################################
# Définition des fixtures:


@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()
    yield client


@pytest.fixture
def fixture_club():
    data = {"name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"}
    return data


@pytest.fixture
def fixture_competition():
    data = {"name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"}
    return data
