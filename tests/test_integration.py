def test_user_flow_integration(client):
    home = client.get('/')
    assert home.status_code == 200

    summary = client.post('/showSummary', data={
        "email": "john@simplylift.co"
    }, follow_redirects=True)

    assert summary.status_code == 200
    assert b"john" in summary.data 