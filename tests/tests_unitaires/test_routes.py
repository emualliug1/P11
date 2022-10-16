
class TestRoutes:

    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_login(self, client, fixture_club):
        response = client.post('/show_summary', data={'email': fixture_club['email']})
        assert response.status_code == 200

    def test_purchase_places(self, client, fixture_club, fixture_competition):
        response = client.post("/purchase_places",
                               data={'competition': fixture_competition['name'],
                                     'club': fixture_club['name'],
                                     'places': '2'},
                               follow_redirects=True)
        assert response.status_code == 200

    def test_competition_reservation(self, client):
        response = client.get('/book/Spring%20Festival/Iron%20Temple', follow_redirects=True)
        assert response.status_code == 200

    def test_logout(self, client):
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
