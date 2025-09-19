import pytest
from db.crud_user import upsert_users, get_users_since

@pytest.fixture
def setup_users(db_manager, sample_users):
    upsert_users(db_manager, sample_users)
    return sample_users

def test_upsert_users(setup_users):
    users = setup_users
    assert len(users) == 2
    for u in users:
        assert u.id is not None

def test_get_users_since(db_manager, setup_users):
    all_users = get_users_since(db_manager, None)
    assert len(all_users) == 2

    future_time = "2999-01-01T00:00:00"
    users = get_users_since(db_manager, future_time)
    assert len(users) == 0
