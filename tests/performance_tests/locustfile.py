from locust import HttpUser, task, between
from server_utils import load_clubs, load_competitions


class LocustTestServer(HttpUser):
    wait_time = between(1, 5)
    competition = load_competitions()[0]
    club = load_clubs()[0]

    def on_start(self):
        self.client.get("/", name=".index")
        self.client.post("/showSummary", data={'email': self.club["email"]}, name=".show_summary")

    @task
    def get_booking(self):
        self.client.get(
            f"/book/{self.competition['name']}/{self.club['name']}",
            name="book"
        )

    # Simulation d'achat sans effet réel
    @task
    def post_booking_simulation(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 0,  # Envoi de "0" pour simuler une demande sans achat
                "club": self.club["name"],
                "competition": self.competition["name"]
            },
            name="purchase_places_simulation"
        )

    @task
    def get_board(self):
        self.client.get("/viewClubPoints", name="view_club_points")
