"""Pytest configuration and shared fixtures for the Mergington High School Activities API tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Original activities data for reset
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team with regular practices and games",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu", "alex@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Join us for soccer practice and friendly matches",
        "schedule": "Tuesdays and Saturdays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["lucas@mergington.edu", "marcus@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "grace@mergington.edu"]
    },
    "Music Band": {
        "description": "Learn to play instruments and perform in concerts",
        "schedule": "Mondays and Fridays, 4:00 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["sarah@mergington.edu", "noah@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["andrew@mergington.edu", "rachel@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["hannah@mergington.edu", "tyler@mergington.edu"]
    }
}


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    activities.clear()
    activities.update(INITIAL_ACTIVITIES)
    yield
    # Cleanup after test
    activities.clear()


@pytest.fixture
def client():
    """Create a TestClient for the FastAPI app."""
    return TestClient(app)
