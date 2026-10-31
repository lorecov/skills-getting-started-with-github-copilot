from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_root_redirects_to_static_index():
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_details():
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert activities["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_new_participant():
    response = client.post(
        "/activities/Basketball%20Team/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up student@mergington.edu for Basketball Team"
    }

    activities = client.get("/activities").json()
    assert "student@mergington.edu" in activities["Basketball Team"]["participants"]


def test_signup_rejects_duplicate_participant():
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_rejects_unknown_activity():
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_removes_participant():
    response = client.delete(
        "/activities/Chess%20Club/participants/michael%40mergington.edu"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_delete_rejects_unknown_participant():
    response = client.delete(
        "/activities/Chess%20Club/participants/unknown%40mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_delete_rejects_unknown_activity():
    response = client.delete(
        "/activities/Unknown%20Club/participants/student%40mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
