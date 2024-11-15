import pytest
from unittest.mock import patch
from server import app
from server_utils import sort_competitions_date, initialize_booked_places, update_booked_places

@pytest.fixture
def client():
    """Fixture for the Flask client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sort_competitions():
    """Fixture for sorting the competitions."""
    return sort_competitions_date

@pytest.fixture
def initialize_bookings():
    """Fixture for initializing bookings."""
    return initialize_booked_places

@pytest.fixture
def update_bookings():
    """Fixture for updating bookings."""
    return update_booked_places

@pytest.fixture
def competition_data():
    """Fixture for competition data."""
    return [
        {"name": "Past Competition", "date": "2020-01-01 10:00:00", "numberOfPlaces": "15"},
        {"name": "Future Competition", "date": "2030-01-01 10:00:00", "numberOfPlaces": "25"}
    ]

@pytest.fixture
def club_data():
    """Fixture for club data."""
    return [
        {"name": "Test Club", "email": "test_club@example.com", "points": "15"},
        {"name": "Test Club 2", "email": "test_club2@example.com", "points": "2"}
    ]

@pytest.fixture
def mock_data(competition_data, club_data, initialize_bookings):
    """
    Patches the global `competitions` and `clubs` data in the server and
    initializes the booked places.
    """
    # Initialize booked places using the function from server_utils
    places_booked = initialize_bookings(competition_data, club_data)

    with patch('server.competitions', competition_data), \
         patch('server.clubs', club_data), \
         patch('server.places_booked', places_booked):  # Mock the global places_booked
        yield places_booked  # Yield the mock data to the test
