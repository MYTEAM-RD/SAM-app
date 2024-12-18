from app.extensions import db
import random
import string
import datetime


class Verification(db.Model):
    id = db.Column(db.Text, primary_key=True)
    type = db.Column(db.Text, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    user_id = db.Column(db.Text, db.ForeignKey("user.id"), unique=False, nullable=True)
    note = db.Column(db.Text, unique=False, nullable=True)

    def __init__(
        self, type: str, user_id: str = None, id: str = None, note: str = None
    ) -> None:
        if not id:
            self.id = "".join(
                random.choices(string.digits, k=5)
            )
        else:
            self.id = id
        self.type = type
        self.created_at = datetime.datetime.utcnow()
        self.user_id = user_id
        self.note = note

    def __repr__(self):
        return f'<Verification "{self.id}">'
