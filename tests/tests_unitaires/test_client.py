class TestClient:

    def test_index(self, client):
        index = client.get('/')
        html = index.data.decode()
        assert "Welcome to the GUDLFT!" in html
        assert index.status_code == 200
