from app.auth_wrapper import token_required, token_required_admin
from app.user import bp
from app.models.user import User
from app.models.verification import Verification
from app.extensions import db
from app.email import Email_with_template
from flask import request, current_app, jsonify
import random
import string
import os
import datetime

##################################################
###                 Login routes               ####
##################################################


@bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data.get("email", None)).first_or_404()
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()
        if user.check_password(data["password"]):
            try:
                return jsonify({"token": user.generate_jwt()}), 200
            except Exception as e:
                current_app.logger.error("canot generate token, error = " + str(e))
                return "bad request", 400
        else:
            return "incorect credentials", 401
    except Exception as e:
        current_app.logger.info("error on login " + str(e))
        return "bad request", 400


@bp.route("/check", methods=["GET"])
@token_required
def check(token):
    return "ok", 200


##################################################
###                 User routes               ####
##################################################


@bp.route("/user/me", methods=["GET"])
@token_required
def get_me(token):
    try:
        user = User.query.filter_by(id=token.get("id", None)).first_or_404()
        return jsonify(user.public_json()), 200
    except Exception as e:
        current_app.logger.error(str(e))
        return "server error", 500


@bp.route("/user", methods=["POST"])
def create():
    try:
        data = request.get_json()
        try:
            user = User(
                email=data["email"],
                name=data.get("name", None),
                password=data["password"],
                company=data.get("company", None),
                company_type=data.get("company_type", None),
                phone=data.get("phone", None),
                credit=int(os.getenv("DEFAULT_CREDIT", 0)),
            )
            db.session.add(user)
            email_verification = Verification(type="email", user_id=user.id)
            db.session.add(email_verification)
            # db.session.add(Verification(type="phone", user_id=user.id))
            Email_with_template(
                os.getenv("SMTP_SENDER", None),
                user.email,
                "verification code",
                "verify_email.html",
                code=email_verification.id,
            ).send()
            db.session.commit()
            return jsonify(user.public_json()), 200
        except Exception as e:
            current_app.logger.error("canot create user, error = " + str(e))
            return "bad request", 400
    except Exception as e:
        current_app.logger.error(str(e))
        return "server error", 500


@bp.route("/user", methods=["PATCH"])
@token_required
def update(token):
    try:
        data = request.get_json()
        # get user by id and modify it
        user = User.query.filter_by(id=token.get("id", None)).first_or_404()
        try:
            if "name" in data:
                user.name = data.get("name")
            if "company" in data:
                user.company = data.get("company")
            if "phone" in data:
                user.phone = data.get("phone")
            if "address" in data:
                user.address = data.get("address")
            if "company_type" in data:
                user.company_type = data.get("company_type")
            if "password" in data:
                user.modify_password(data.get("password"))
                Email_with_template(
                    os.getenv("SMTP_SENDER", None),
                    user.email,
                    "project_name verification code",
                    "user_password.html",
                ).send()
            user.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            return user.public_json(), 200
        except Exception as e:
            current_app.logger.error(str(e))
            return "bad request", 400
    except Exception as e:
        current_app.logger.error(str(e))
        return "server error", 500


@bp.route("/user", methods=["DELETE"])
@token_required
def delete(token):
    try:
        # get user by id and delete it
        user = User.query.filter_by(id=token.get("id", None)).first_or_404()
        try:
            db.session.delete(user)
            db.session.commit()
            Email_with_template(
                os.getenv("SMTP_SENDER", None),
                user.email,
                "account deleted",
                "user_delete.html",
            ).send()
            return user.public_json(), 200
        except Exception as e:
            current_app.logger.error(str(e))
            return "bad request", 400
    except Exception as e:
        current_app.logger.error(str(e))
        return "server error", 500


@bp.route("/user/email", methods=["PATCH"])
@token_required
def update_email(token):
    try:
        data = request.get_json()
        # get user by id and modify it
        user = User.query.filter_by(id=token.get("id", None)).first_or_404()
        try:
            user.email = data["email"]
            user.email_verified = False
            user.updated_at = datetime.datetime.utcnow()
            email_verification = Verification(type="email", user_id=user.id)
            db.session.add(email_verification)
            # db.session.add(Verification(type="phone", user_id=user.id))
            Email_with_template(
                os.getenv("SMTP_SENDER", None),
                user.email,
                "verification code",
                "verify_email.html",
                code=email_verification.id,
            ).send()
            db.session.commit()
            return user.public_json(), 200
        except Exception as e:
            current_app.logger.error(str(e))
            return "bad request", 400
    except Exception as e:
        current_app.logger.error(str(e))
        return "server error", 500


@bp.route("/trouble/forgot_email", methods=["GET"])
def forgot_email():
    user = User.query.filter_by(email=request.args.get("email")).first_or_404()
    verification = Verification(
        "password_forgot",
        user.id,
        id="".join(random.choices(string.ascii_lowercase + string.digits, k=25)),
    )
    db.session.add(verification)
    try:
        Email_with_template(
            os.getenv("SMTP_SENDER", None),
            user.email,
            "Reset your password",
            "user_password_reset.html",
            password_reset_url=os.environ.get("ACTION_URL_RESET_PASSWORD"),
            code=verification.id,
        ).send()
    except Exception as e:
        current_app.logger.critical(
            f"error [email to reset password can't be sent error = {str(e)}]"
        )
        return "server error", 500
    db.session.commit()
    return "Email sended to user email.", 200


@bp.route("/trouble/forgot_email", methods=["POST"])
def reset_email_with_code():
    data = request.get_json()
    verification = Verification.query.filter_by(id=data.get("code")).first_or_404()
    user = User.query.filter_by(id=verification.user_id).first_or_404()
    try:
        user.modify_password(data["password"])
        user.updated_at = datetime.datetime.utcnow()
        try:
            Email_with_template(
                os.getenv("SMTP_SENDER", None),
                user.email,
                "Click here to reset your password",
                "user_password.html",
            ).send()
        except:
            pass
        db.session.delete(verification)
        db.session.commit()
    except KeyError as e:
        return f"Missing required key: {str(e)}", 400
    except Exception as e:
        current_app.logger.error(str(e))
        return "bad request", 400
    return "Password has been succesfully modified.", 200


##################################################
###          User management routes           ####
##################################################


@bp.route("/user/<user_id>", methods=["DELETE"])
@token_required_admin
def delete_user(token, user_id):
    try:
        # get user by id and delete it
        user = User.query.filter_by(id=user_id).first_or_404()
        try:
            db.session.delete(user)
            db.session.commit()
            Email_with_template(
                os.getenv("SMTP_SENDER", None),
                user.email,
                "account deleted",
                "user_delete.html",
            ).send()
            return user.public_json(), 200
        except Exception as e:
            current_app.logger.error(str(e))
            return "bad request", 400
    except Exception as e:
        current_app.logger.error(str(e))
        return "server error", 500
