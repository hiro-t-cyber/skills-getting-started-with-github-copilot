"""Tests for the root endpoint (GET /)."""

import pytest


class TestRootEndpoint:
    """Test suite for the root endpoint redirect."""

    def test_redirect_to_index(self, client):
        """Verify root endpoint redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
