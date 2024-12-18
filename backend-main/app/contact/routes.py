from app.auth_wrapper import token_required
from app.email import Email_with_template
from app.models.analyse import Analyse
from app.user import bp
from app.models.user import User
from app.extensions import db
from flask import request, current_app, jsonify
import os


@bp.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.get_json()
        if not "from" in data:
            return "you have to provide a from", 400
        if not "subject" in data:
            return "you have to provide an subject", 400
        if not "phone" in data:
            return "you have to provide an phone", 400
        if not "content" in data:
            return "you have to provide an content", 400
        try:
            Email_with_template(
                os.getenv("SMTP_SENDER", None),
                "contact@myteam.ai",
                data.get("subject"),
                "contact.html",
                origin=data.get("from"),
                object=data.get("subject"),
                phone=data.get("phone"),
                content=data.get("content"),
            ).send()
            return "sended", 200
        except Exception as e:
            current_app.logger.info("can't send email " + str(e))
            return "bad request", 400
    except Exception as e:
        current_app.logger.info("error on contact " + str(e))
        return "bad request", 400
