from app.extensions import db
import datetime
import bcrypt
import uuid
import jwt
import os
import stripe
import json

class User(db.Model):
    id = db.Column(db.Text, primary_key=True)
    customer_id = db.Column(db.Text, unique=True, nullable=True)
    type = db.Column(db.String(100), unique=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    phone = db.Column(db.Text, unique=False, nullable=True)
    address = db.Column(db.Text, unique=False, nullable=True)
    company_type = db.Column(db.Text, unique=False, nullable=True)
    name = db.Column(db.Text, unique=False)
    password = db.Column(db.Text, unique=False)
    company = db.Column(db.Text, unique=False, nullable=True)
    credit = db.Column(db.Text, unique=False, default=0)
    subscription_credit = db.Column(db.Text, unique=False, default=0)
    email_verified = db.Column(db.Boolean, unique=False, default=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    updated_at = db.Column(db.DateTime, unique=False, nullable=False)
    last_login = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(
        self,
        email,
        name,
        password,
        company: str = None,
        credit: int = 0,
        email_verified=False,
        created_at=datetime.datetime.utcnow(),
        id=None,
        _type="user",
        phone: str = None,
        address: str = None,
        company_type: str = None,
        suscription_credit: str = "[]",
        customer_id: str = None,
    ):
        self.id = id if id is not None else str(uuid.uuid4())
        self.type = _type
        self.email = email
        self.name = name
        self.company = company
        self.credit = credit
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
        self.email_verified = email_verified
        self.created_at = created_at
        self.updated_at = created_at
        self.last_login = created_at
        self.phone = phone
        self.address = address
        self.company_type = company_type
        self.subscription_credit = suscription_credit
        self.customer_id = customer_id
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def modify_password(self, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def generate_jwt(self) -> dict:
        if self.type == "admin":
            scope = "admin"
        else:
            scope = "user"
        encoded_jwt = jwt.encode(
            {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=14),
                "iat": datetime.datetime.utcnow(),
                "nbf": datetime.datetime.utcnow(),
                "scope": scope,
                "id": self.id,
                "email_verified": self.email_verified,
            },
            os.environ.get("SECRET_KEY"),
            algorithm="HS256",
        )
        return encoded_jwt
    
    def remove_n_credit(self, n: int):
        if int(self.get_avaible_subscription_credit()) >= n:
            data = json.loads(self.subscription_credit)
            new_data = data[n:]
            self.subscription_credit = json.dumps(new_data)
            db.session.commit()
            return True
        else :
            if int(self.credit) >= n:
                self.credit = int(self.credit) - n
                db.session.commit()
                return True
            
    def add_n_subscription_credit(self, n: int):
        data = json.loads(self.subscription_credit)
        futureDate = datetime.datetime.utcnow()+datetime.timedelta(days=30)
        data += [futureDate.timestamp()] * n
        self.subscription_credit = json.dumps(data)
        db.session.commit()
            
    
    def get_avaible_subscription_credit(self):
        data = json.loads(self.subscription_credit)
        total = 0
        new_data = []
        for item in data:
            if item > datetime.datetime.utcnow().timestamp():
                total += 1 
                new_data.append(item)
        self.subscription_credit = json.dumps(new_data)
        db.session.commit()
        return total

    def public_json(self):
        return {
            "id": str(self.id),
            "email": str(self.email),
            "name": str(self.name),
            "company": str(self.company),
            "credit": str(int(self.credit) + self.get_avaible_subscription_credit()),
            "company_type": str(self.company_type),
            "phone": str(self.phone),
            "address": str(self.address),
            "email_verified": str(self.email_verified),
        }

    def update_subscription_credit(self, credit: int):
        self.subscription_credit = credit
        db.session.commit()

    def get_customer_id(self, create_if_not_exist: bool = True) -> str:
        if create_if_not_exist:
            if self.customer_id is None:
                customer = stripe.Customer.create(
                    email=self.email,
                    name=self.name,
                    phone=self.phone,
                    metadata={"user_id": self.id},
                )
                self.customer_id = customer.id
                db.session.commit()
                return self.customer_id
            return self.customer_id
        else:
            return self.customer_id

    def __repr__(self):
        return f'<User "{self.email}">'
