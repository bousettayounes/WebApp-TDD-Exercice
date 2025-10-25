def test_access_welcome_without_email(client):
    response = client.post('/showSummary', data={}, follow_redirects=True)
    assert b"Please enter your secretary email" in response.data


def test_access_admin_without_login(client):
    response = client.get('/admin', follow_redirects=True)
    assert b"Admin Login" in response.data

