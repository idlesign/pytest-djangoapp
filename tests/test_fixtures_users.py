
def test_user_create(user_create):

    assert not user_create().is_superuser
    assert user_create(superuser=True).is_superuser
    assert user_create(anonymous=True).is_anonymous


def test_user_model(user_model):

    assert user_model


def test_user(user):

    assert user
    assert user.password_plain == 'password'
