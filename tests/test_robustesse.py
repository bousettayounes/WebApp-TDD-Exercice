def test_multiple_requests_robustesse(client):
    for _ in range(50): 
        response = client.get('/')
        assert response.status_code == 200
