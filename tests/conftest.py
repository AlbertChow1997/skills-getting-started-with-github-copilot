"""Pytest configuration and fixtures"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to a clean state before each test"""
    activities.clear()
    activities.update({
        "Tennis": {"description": "Learn to play tennis", "participants": []},
        "Basketball": {"description": "Play basketball with friends", "participants": []},
        "Volleyball": {"description": "Join our volleyball team", "participants": []},
        "Soccer": {"description": "Play soccer on the field", "participants": []},
        "Drama Club": {"description": "Perform in theatrical productions", "participants": []},
        "Painting": {"description": "Create beautiful artwork with acrylics and oils", "participants": []},
        "Photography": {"description": "Explore the art of digital photography", "participants": []},
        "Debate Club": {"description": "Compete in debate tournaments", "participants": []},
        "Robotics": {"description": "Build and program robots", "participants": []},
        "Chess Club": {"description": "Master strategy and tactics in chess", "participants": []},
    })
