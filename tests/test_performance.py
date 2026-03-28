import time

def test_home_performance(client):
    start = time.time()
    response = client.get('/')
    end = time.time()

    elapsed = end - start

    assert response.status_code == 200
    assert elapsed < 0.3  
