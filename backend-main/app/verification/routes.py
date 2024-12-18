from app.auth_wrapper import token_required
from app.email import Email_with_template
from app.verification import bp
from app.models.user import User
from app.models.verification import Verification
from app.extensions import db
from flask import request, current_app, jsonify
from sqlalchemy import and_
import jwt
import os
import datetime
import json


# verify Email
@bp.route("/verify/email", methods=["GET"])
def verify_email():
    verif = Verification.query.filter(
        and_(Verification.id == request.args.get("code"), Verification.type == "email")
    ).first_or_404()
    user = User.query.filter_by(id=verif.user_id).first_or_404()
    try:
        user.email_verified = True
        db.session.delete(verif)
        db.session.commit()
        return jsonify({"token": user.generate_jwt()}), 200
    except Exception as e:
        current_app.logger.error("Email verification failed error = " + str(e))
        return jsonify(message="Email verification failed"), 500


# new Email
@bp.route("/verify/new/email", methods=["GET"])
def ask_new_verify_email():
    user = User.query.filter_by(email=request.args.get("email")).first_or_404()
    try:
        verif = Verification(user_id=user.id, type="email")
        db.session.add(verif)
        Email_with_template(
                os.getenv("SMTP_SENDER", None),
                user.email,
                "verification code",
                "verify_email.html",
                code=verif.id,
            ).send()
        db.session.commit()
        return "generated a new one", 200
    except Exception as e:
        current_app.logger.error("Email verification renew error = " + str(e))
        return jsonify(message="Email verification renew"), 500
