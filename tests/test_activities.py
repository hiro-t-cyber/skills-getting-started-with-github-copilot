"""Tests for the activities endpoint (GET /activities)."""

import pytest


class TestActivitiesEndpoint:
    """Test suite for the activities list endpoint."""

    def test_get_all_activities_returns_correct_structure(self, client):
        """Verify /activities returns all activities with correct structure."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) == 9
        
        # Verify each activity has required fields
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_activities_match_initial_data(self, client):
        """Verify initial activities data matches expected values."""
        response = client.get("/activities")
        activities = response.json()
        
        # Verify Chess Club exists and has expected data
        assert "Chess Club" in activities
        chess_club = activities["Chess Club"]
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
        assert chess_club["max_participants"] == 12
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
        
        # Verify all 9 activities are present
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Soccer Club", "Art Studio", "Music Band", "Science Club", "Debate Team"
        ]
        for activity in expected_activities:
            assert activity in activities
