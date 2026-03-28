def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<form" in response.data
    
def test_home_post_valid(client):
    response = client.post('/showSummary', data={"email":"john@simplylift.co"}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome" in response.data  