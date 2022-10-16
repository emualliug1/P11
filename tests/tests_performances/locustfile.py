from locust import HttpUser, task, between


class WebSiteUser(HttpUser):
    wait_time = between(5, 15)
    club = {"name": "admin",
            "email": "a@a",
            "points": "500"}

    competition = {
            "name": "test02",
            "date": "2022-12-22 13:30:00",
            "numberOfPlaces": "16"}

    def on_start(self):
        self.client.get("/")
        self.client.post("/show_summary", {'email': self.club["email"]})

    @task
    def get_booking(self):
        self.client.get(f"/book/{self.competition['name']}/{self.club['name']}")

    @task
    def post_booking(self):
        self.client.post("/purchase_places", {"club": self.club["name"],
                                            "competition": self.competition["name"],
                                            "places": 1})

    @task
    def club_points(self):
        self.client.get("/tableau_points")
