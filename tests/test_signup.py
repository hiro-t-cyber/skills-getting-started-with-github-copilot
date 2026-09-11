"""Tests for the signup endpoint (POST /activities/{activity_name}/signup)."""

import pytest


class TestSignup:
    """Test suite for activity signup functionality."""

    def test_successful_signup(self, client):
        """Verify a new student can successfully sign up for an activity."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "alice@mergington.edu"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Signed up alice@mergington.edu for Chess Club"
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "alice@mergington.edu" in activities["Chess Club"]["participants"]

    def test_signup_updates_participant_count(self, client):
        """Verify participant count increases with each signup."""
        # Initial count for Programming Class
        response = client.get("/activities")
        initial_count = len(response.json()["Programming Class"]["participants"])
        assert initial_count == 2
        
        # Sign up first student
        client.post(
            "/activities/Programming Class/signup",
            params={"email": "student1@mergington.edu"}
        )
        response = client.get("/activities")
        assert len(response.json()["Programming Class"]["participants"]) == initial_count + 1
        
        # Sign up second student
        client.post(
            "/activities/Programming Class/signup",
            params={"email": "student2@mergington.edu"}
        )
        response = client.get("/activities")
        assert len(response.json()["Programming Class"]["participants"]) == initial_count + 2

    def test_duplicate_signup_rejected(self, client):
        """Verify duplicate signup attempts are rejected with 400 status."""
        email = "duplicate_tester@mergington.edu"
        
        # First signup should succeed
        response = client.post(
            "/activities/Gym Class/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Second signup with same email should fail
        response = client.post(
            "/activities/Gym Class/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_to_nonexistent_activity(self, client):
        """Verify signup to nonexistent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_with_empty_email(self, client):
        """Verify signup with empty email string."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": ""}
        )
        # Currently accepts empty string (no email validation implemented)
        # This documents current behavior
        assert response.status_code == 200

    def test_signup_to_different_activities(self, client):
        """Verify same student can sign up for multiple activities."""
        email = "multiactivity@mergington.edu"
        
        # Sign up for Chess Club
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Sign up for Gym Class
        response2 = client.post(
            "/activities/Gym Class/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify student in both activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Gym Class"]["participants"]
