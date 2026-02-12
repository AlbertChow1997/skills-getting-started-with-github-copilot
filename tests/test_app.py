"""Tests for the FastAPI application"""

import pytest


def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Tennis" in data
    assert "Basketball" in data
    assert len(data) == 10


def test_get_activities_structure(client):
    """Test that activities have the correct structure"""
    response = client.get("/activities")
    data = response.json()
    for activity_name, activity_data in data.items():
        assert "description" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_signup_for_activity(client):
    """Test signing up for an activity"""
    email = "student@mergington.edu"
    response = client.post(f"/activities/Tennis/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]


def test_signup_adds_participant(client):
    """Test that signup actually adds participant to the activity"""
    email = "student@mergington.edu"
    client.post(f"/activities/Tennis/signup?email={email}")
    
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Tennis"]["participants"]


def test_signup_duplicate_fails(client):
    """Test that signing up twice for the same activity fails"""
    email = "student@mergington.edu"
    
    # First signup should succeed
    response1 = client.post(f"/activities/Tennis/signup?email={email}")
    assert response1.status_code == 200
    
    # Second signup should fail
    response2 = client.post(f"/activities/Tennis/signup?email={email}")
    assert response2.status_code == 400
    data = response2.json()
    assert "already signed up" in data["detail"]


def test_signup_nonexistent_activity(client):
    """Test signing up for a nonexistent activity"""
    email = "student@mergington.edu"
    response = client.post(f"/activities/Nonexistent/signup?email={email}")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]


def test_multiple_students_signup(client):
    """Test that multiple students can sign up for the same activity"""
    emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    
    for email in emails:
        response = client.post(f"/activities/Tennis/signup?email={email}")
        assert response.status_code == 200
    
    response = client.get("/activities")
    activities = response.json()
    assert len(activities["Tennis"]["participants"]) == 3
    for email in emails:
        assert email in activities["Tennis"]["participants"]


def test_remove_participant(client):
    """Test removing a participant from an activity"""
    email = "student@mergington.edu"
    
    # First sign up
    client.post(f"/activities/Tennis/signup?email={email}")
    
    # Then remove
    response = client.delete(f"/activities/Tennis/participants/{email}")
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]
    
    # Verify removal
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities["Tennis"]["participants"]


def test_remove_nonexistent_participant(client):
    """Test removing a participant that doesn't exist"""
    email = "nonexistent@mergington.edu"
    response = client.delete(f"/activities/Tennis/participants/{email}")
    assert response.status_code == 404


def test_remove_from_nonexistent_activity(client):
    """Test removing a participant from a nonexistent activity"""
    email = "student@mergington.edu"
    response = client.delete(f"/activities/Nonexistent/participants/{email}")
    assert response.status_code == 404


def test_signup_and_remove_flow(client):
    """Test the complete flow of signing up and removing"""
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Both students sign up for Tennis
    client.post(f"/activities/Tennis/signup?email={email1}")
    client.post(f"/activities/Tennis/signup?email={email2}")
    
    # Remove first student
    response = client.delete(f"/activities/Tennis/participants/{email1}")
    assert response.status_code == 200
    
    # Verify only second student remains
    response = client.get("/activities")
    activities = response.json()
    assert len(activities["Tennis"]["participants"]) == 1
    assert email2 in activities["Tennis"]["participants"]
    assert email1 not in activities["Tennis"]["participants"]
    
    # Second student can now sign up for another activity
    response = client.post(f"/activities/Basketball/signup?email={email2}")
    assert response.status_code == 200
