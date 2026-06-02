import sys
from pathlib import Path
import copy

from fastapi.testclient import TestClient
import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from app import app, activities  # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities state before and after each test."""
    # Arrange: save original state
    original_activities = copy.deepcopy(activities)
    yield
    # Assert/Cleanup: restore original state after test
    activities.clear()
    activities.update(original_activities)
