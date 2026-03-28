from server import loadClubs

def test_load_clubs_unit():
    clubs = loadClubs()
    assert isinstance(clubs, list)
    assert len(clubs) > 0
    assert "name" in clubs[0]
