import pytest
from db.crud_user import upsert_users, get_users_since

@pytest.fixture
def setup_users(db_instance, sample_users):
    """Insert sample users into the database."""
    upsert_users(db_instance, sample_users)
    return sample_users

def test_upsert_users(setup_users):
    users = setup_users
    assert len(users) == 2
    for u in users:
        assert u.id is not None

def test_get_users_since(db_instance, setup_users):
    all_users = get_users_since(db_instance, None)
    assert len(all_users) == 2

    future_time = "2999-01-01T00:00:00"
    empty_users = get_users_since(db_instance, future_time)
    assert len(empty_users) == 0
