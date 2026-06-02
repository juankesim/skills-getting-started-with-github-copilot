"""FastAPI backend tests using AAA (Arrange-Act-Assert) pattern."""


def test_root_redirects_to_static_index(client):
    """Test that root endpoint redirects to static index.html"""
    # Arrange
    # Act
    response = client.get("/", allow_redirects=False)
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_list(client):
    """Test that GET /activities returns all activities with participants."""
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_new_participant(client):
    """Test that a new participant can sign up for an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "new_student@mergington.edu"
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    # Verify participant was added
    get_response = client.get("/activities")
    assert email in get_response.json()[activity_name]["participants"]


def test_signup_for_activity_returns_400_when_already_signed_up(client):
    """Test that duplicate signup returns 400 error."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_from_activity(client):
    """Test that a participant can be removed from an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    # Verify participant was removed
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity_name]["participants"]


def test_remove_participant_returns_404_for_missing_participant(client):
    """Test that removing non-existent participant returns 404."""
    # Arrange
    activity_name = "Chess Club"
    email = "not_registered@mergington.edu"
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_unknown_activity_returns_404(client):
    """Test that signing up for unknown activity returns 404."""
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_from_unknown_activity_returns_404(client):
    """Test that removing from unknown activity returns 404."""
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
