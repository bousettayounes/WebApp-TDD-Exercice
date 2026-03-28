import pytest

def test_admin_page_accessible(client):
    response = client.get('/admin')
    assert response.status_code == 200
    assert b"<form" in response.data
    
def test_admin_wrong_credentials(client):
    response = client.post('/admin', data={
        "email":"wrong",
        "password":"wrong"
    }, follow_redirects=True)

    assert b"Unauthorized" in response.data or response.status_code == 403

@pytest.mark.parametrize("email", [
    "john@simplylift.co",
    "kate@shelifts.co.uk",
    "admin@irontemple.com",
    "admin@admin.com"
])
def test_parametrized_clients(client, email):
    response = client.post('/showSummary', data={"email": email}, follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.parametrize("email,password,authorized", [
    ("admin","admin", True),
    ("admin","wrong", False),
    ("wrong","admin", False),
    ("wrong","wrong", False),
])
def test_admin_combinations(client, email, password, authorized):
    response = client.post('/admin', data={
        "email":email,
        "password":password
    }, follow_redirects=True)

    if authorized:
        assert b"Welcome Admin" in response.data
    else:
        assert b"Unauthorized" in response.data or response.status_code == 403
import subprocess
import webbrowser
import os

def run_pytest():
    report_path = "report.html"

    subprocess.run(["pytest", "--html=" + report_path, "--self-contained-html"])

    if os.path.exists(report_path):
        webbrowser.open(report_path)

if __name__ == "__main__":
    run_pytest()