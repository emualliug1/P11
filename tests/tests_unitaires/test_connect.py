class TestConnect:

    def test_connect(self, client, fixture_club):
        """test de connexion avec l'adresse d'un secrétaire"""
        data = {'email': fixture_club['email']}
        response = client.post('/show_summary', data=data)
        assert response.status_code == 200

    def test_connect_with_bad_email(self, client):
        """test de connexion avec une adresse mail non connu"""
        data = {'email': 'test@gmail.com'}
        response = client.post('/show_summary', data=data)
        expected_error = "Impossible de vous authentifier adresse mail inconnu."
        data = response.data.decode()
        assert response.status_code == 200
        assert expected_error in data

    def test_connect_with_no_email(self, client):
        """test de connexion avec aucune adresse mail"""
        data = {'email': ''}
        response = client.post('/show_summary', data=data)
        expected_error = 'Veuillez rentrer une adresse mail.'
        data = response.data.decode()
        assert response.status_code == 200
        assert expected_error in data
