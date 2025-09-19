import pytest
from db.crud_track import upsert_tracks, get_tracks_since, select_tracks_by_ids
from db.crud_user import upsert_users
from db.crud_playlist import upsert_playlists

@pytest.fixture
def setup_tracks(db_manager, sample_users, sample_playlists, sample_tracks):
    upsert_users(db_manager, sample_users)
    upsert_playlists(db_manager, sample_playlists)
    upsert_tracks(db_manager, sample_tracks)
    return sample_tracks

def test_upsert_tracks(setup_tracks):
    tracks = setup_tracks
    assert len(tracks) == 2
    for t in tracks:
        assert t.id is not None

def test_get_tracks_since(db_manager, setup_tracks):
    all_tracks = get_tracks_since(db_manager, None)
    assert len(all_tracks) == 2

    future_time = "2999-01-01T00:00:00"
    empty_tracks = get_tracks_since(db_manager, future_time)
    assert len(empty_tracks) == 0

def test_select_tracks_by_ids(db_manager, setup_tracks):
    tracks = setup_tracks
    track_id = tracks[0].id
    result = select_tracks_by_ids(db_manager, [track_id])
    assert len(result) == 1
    assert result[0]["id"] == track_id

    empty_result = select_tracks_by_ids(db_manager, [])
    assert empty_result == []
