import pytest
import os
import jwt
import datetime
import json

from app import create_app, db
from app.models.analyse import Analyse
from app.models.user import User
from app.models.verification import Verification
from config import Config


def generate_token_user(user: User):
    encoded_jwt = jwt.encode(
        {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=14),
            "iat": datetime.datetime.utcnow(),
            "nbf": datetime.datetime.utcnow(),
            "scope": "user",
            "id": user.id,
            "email_verified": user.email_verified,
        },
        os.environ.get("SECRET_KEY"),
        algorithm="HS256",
    )
    return "Bearer " + encoded_jwt


def generate_token_admin(user: User):
    encoded_jwt = jwt.encode(
        {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=14),
            "iat": datetime.datetime.utcnow(),
            "nbf": datetime.datetime.utcnow(),
            "scope": "admin",
            "id": user.id,
            "email_verified": user.email_verified,
        },
        os.environ.get("SECRET_KEY"),
        algorithm="HS256",
    )
    return "Bearer " + encoded_jwt


@pytest.fixture
def client():
    conf = Config()
    app = create_app(conf)
    client = app.test_client()
    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client_with_user():
    conf = Config()
    app = create_app(conf)
    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
        db.session.add(user)
        db.session.commit()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client_with_user_and_analysis():
    conf = Config()
    app = create_app(conf)
    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
        user2 = User(
            "impostor@gmail.com",
            "impostor",
            "Password1",
            email_verified=True,
            id="9ab49c23-120b-4294-89df-27ad88deaf90",
        )
        analyse = Analyse(
            b"test",
            filename="fake data.pdf",
            created_by=user.id,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
        db.session.add(user)
        db.session.add(user2)
        db.session.add(analyse)
        db.session.commit()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client_with_user_and_multiples_analysis():
    conf = Config()
    app = create_app(conf)
    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
        user2 = User(
            "impostor@gmail.com",
            "impostor",
            "Password1",
            email_verified=True,
            id="9ab49c23-120b-4294-89df-27ad88deaf90",
        )
        analyse = Analyse(
            b"test",
            filename="fake data.pdf",
            created_by=user.id,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
        analyse2 = Analyse(
            b"test",
            filename="fake data.pdf",
            created_by=user.id,
            id="3ab49c23-120b-4294-89df-27ad88deaf10",
        )
        db.session.add(user)
        db.session.add(user2)
        db.session.add(analyse)
        db.session.add(analyse2)
        db.session.commit()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client_with_admin():
    conf = Config()
    app = create_app(conf)
    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = User(
            "test@gmail.com",
            "lucas",
            "Password1",
            _type="admin",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
        db.session.add(user)
        db.session.commit()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client_with_user_unverified():
    conf = Config()
    app = create_app(conf)
    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=False,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
        db.session.add(user)
        db.session.add(Verification("email", user_id=user.id, id="0000"))
        db.session.commit()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client_with_user_password_forgotten():
    conf = Config()
    app = create_app(conf)
    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = User(
            "test@gmail.com",
            "lucas",
            "Password1",
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
        db.session.add(user)
        db.session.add(Verification("password_forgot", user_id=user.id, id="5555"))
        db.session.commit()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client_with_user_credited():
    conf = Config()
    app = create_app(conf)
    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
        db.session.add(user)
        db.session.commit()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client_with_user_sub_credited():
    conf = Config()
    app = create_app(conf)
    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=0,
            suscription_credit=json.dumps([datetime.datetime.utcnow().timestamp()+10000,datetime.datetime.utcnow().timestamp()+10000]),
        )
        db.session.add(user)
        db.session.commit()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client_with_user_sub_outdated():
    conf = Config()
    app = create_app(conf)
    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=0,
            suscription_credit=json.dumps([datetime.datetime.utcnow().timestamp()-10000,datetime.datetime.utcnow().timestamp()-10000]),
        )
        db.session.add(user)
        db.session.commit()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client_with_user_payment_wating():
    conf = Config()
    app = create_app(conf)
    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
        verif = Verification(
            "payment",
            user_id=user.id,
            id="5555",
            note=json.dumps([{"quantity": 1, "amount": 5, "type": "payment"}]),
        )
        verif2 = Verification(
            "subscription",
            user_id=user.id,
            id="6666",
            note=json.dumps([{"quantity": 1, "amount": 3, "type": "subscription"}]),
        )
        verif3 = Verification(
            "payment",
            user_id=user.id,
            id="7777",
            note=json.dumps([{"quantity": 2, "amount": 5, "type": "payment"}]),
        )
        verif4 = Verification(
            "payment",
            user_id=user.id,
            id="8888",
            note=json.dumps(
                [
                    {"quantity": 2, "amount": 5, "type": "payment"},
                    {"quantity": 1, "amount": 20, "type": "subscription"},
                ]
            ),
        )
        db.session.add(verif)
        db.session.add(verif2)
        db.session.add(verif3)
        db.session.add(verif4)
        db.session.add(user)
        db.session.commit()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()
