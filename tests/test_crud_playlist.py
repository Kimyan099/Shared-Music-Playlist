import pytest
from db.crud_playlist import upsert_playlists, get_playlists_since

@pytest.fixture
def setup_playlists(db_manager, sample_users, sample_playlists):
    # Make sure users exist first
    from db.crud_user import upsert_users
    upsert_users(db_manager, sample_users)
    upsert_playlists(db_manager, sample_playlists)
    return sample_playlists

def test_upsert_playlists(setup_playlists):
    playlists = setup_playlists
    assert len(playlists) == 2
    for p in playlists:
        assert p.id is not None

def test_get_playlists_since(db_manager, setup_playlists):
    playlists = get_playlists_since(db_manager, None)
    assert len(playlists) == 2

    future_time = "2999-01-01T00:00:00"
    playlists = get_playlists_since(db_manager, future_time)
    assert len(playlists) == 0
