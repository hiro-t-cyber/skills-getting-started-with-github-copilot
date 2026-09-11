"""Tests for the participant removal endpoint (DELETE /activities/{activity_name}/remove)."""

import pytest


class TestRemoval:
    """Test suite for participant removal functionality."""

    def test_successful_removal(self, client):
        """Verify a participant can be successfully removed from an activity."""
        # Michael is initially in Chess Club
        response = client.delete(
            "/activities/Chess Club/remove",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

    def test_removal_decreases_count(self, client):
        """Verify participant count decreases after removal."""
        # Gym Class initially has 2 participants
        response = client.get("/activities")
        initial_count = len(response.json()["Gym Class"]["participants"])
        assert initial_count == 2
        
        # Remove john@mergington.edu
        response = client.delete(
            "/activities/Gym Class/remove",
            params={"email": "john@mergington.edu"}
        )
        assert response.status_code == 200
        
        # Verify count decreased
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert len(activities["Gym Class"]["participants"]) == initial_count - 1

    def test_remove_nonexistent_participant(self, client):
        """Verify removing nonexistent participant returns 404."""
        response = client.delete(
            "/activities/Chess Club/remove",
            params={"email": "nonexistent@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_remove_from_nonexistent_activity(self, client):
        """Verify removing from nonexistent activity returns 404."""
        response = client.delete(
            "/activities/Nonexistent Activity/remove",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_add_and_remove_cycle(self, client):
        """Verify add → remove → add cycle works correctly."""
        email = "cycle_tester@mergington.edu"
        activity = "Art Studio"
        
        # Sign up
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify added
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity]["participants"]
        
        # Remove
        response = client.delete(
            f"/activities/{activity}/remove",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify removed
        activities_response = client.get("/activities")
        assert email not in activities_response.json()[activity]["participants"]
        
        # Sign up again
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify re-added
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity]["participants"]

    def test_remove_all_participants(self, client):
        """Verify multiple participants can be removed from one activity."""
        activity = "Music Band"
        
        # Initially has 2 participants: sarah@mergington.edu, noah@mergington.edu
        # Remove first
        response = client.delete(
            f"/activities/{activity}/remove",
            params={"email": "sarah@mergington.edu"}
        )
        assert response.status_code == 200
        
        # Remove second
        response = client.delete(
            f"/activities/{activity}/remove",
            params={"email": "noah@mergington.edu"}
        )
        assert response.status_code == 200
        
        # Verify activity is empty
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert len(activities[activity]["participants"]) == 0
