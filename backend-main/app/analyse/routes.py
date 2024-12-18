from app.auth_wrapper import token_required
from app.models.analyse import Analyse
from app.user import bp
from app.models.user import User
from app.extensions import db
from flask import request, current_app, jsonify


@bp.route("/analyse", methods=["POST"])
@token_required
def create_analyse(token):
    try:
        if (
            "file" not in request.files
        ):  # Check if 'file' key is present in the request files
            return "you have to provide a file", 400
        file = request.files["file"]  # Get the file from the request

        try:
            try:
                file_bytes = file.read()  # Read the content of the file
            except Exception as e:
                current_app.logger.info(
                    "can't read file " + str(e)
                )  # Log an error if file reading fails
                return "bad request", 400

            user = User.query.filter_by(
                id=token.get("id", None)
            ).first_or_404()  # Get the user based on the provided token

            if (
                int(user.credit) + int(user.get_avaible_subscription_credit())
            ) < 1:  # Check if the user has enough credit
                return "not enough credit", 403

            # Create a new Analyse object with the file content, filename, and creator ID
            analyse = Analyse(
                file_bytes, filename=file.filename, created_by=token["id"]
            )

            try:
                analyse.run_analyse()  # Run the analysis on the file
            except Exception as e:
                current_app.logger.info(
                    "can't run analyse " + str(e)
                )  # Log an error if analysis fails
                return "can't run analyse try again later", 500

            user.remove_n_credit(1)

            db.session.add(analyse)  # Add the new analysis to the database session
            db.session.commit()  # Commit the changes to the database

            db.session.add(user)  # Add the user to the database session
            db.session.commit()  # Commit the changes to the database

            return (
                jsonify(analyse.public_json()),
                200,
            )  # Return the public JSON representation of the analysis

        except Exception as e:
            current_app.logger.info(
                "can't create analyse please retry" + str(e)
            )  # Log an error if analysis creation fails
            return "bad request", 400

    except Exception as e:
        current_app.logger.info(
            "error on create analyse " + str(e)
        )  # Log an error if there is an exception
        return "bad request", 400


@bp.route("/analyse", methods=["GET"])
@token_required
def get_all_user_analyse(token):
    try:
        analyse = Analyse.query.filter_by(created_by=token.get("id", None)).all()
        return jsonify([e.public_json() for e in analyse]), 200
    except Exception as e:
        current_app.logger.info("error on get all user analyse " + str(e))
        return "bad request", 400


@bp.route("/analyse/<id>", methods=["GET"])
@token_required
def download_analyse(id, token):
    analyse = Analyse.query.filter_by(id=id).first_or_404()
    try:
        if not "admin" in token.get("scope", None):
            if analyse.created_by != token.get("id", None):
                current_app.logger.warning(
                    f"user attempt to download analyse he didn't create, user_id={token.get('id',None)}, analyse_id={id}"
                )
                return "not authorized", 401
        return (
            analyse.get_file(),
            200,
            {
                "Content-Type": "application/octet-stream",
                "Content-Disposition": "attachment; filename=" + analyse.filename,
            },
        )
    except Exception as e:
        current_app.logger.info("error on get analyse " + str(e))
        return "bad request", 400


@bp.route("/analyse/<id>/info", methods=["GET"])
@token_required
def get_info_on_analyse(id, token):
    analyse = Analyse.query.filter_by(id=id).first_or_404()
    try:
        if not "admin" in token.get("scope", None):
            if analyse.created_by != token.get("id", None):
                current_app.logger.warning(
                    f"user attempt to get info on analyse he didn't create, user_id={token.get('id',None)}, analyse_id={id}"
                )
                return "not authorized", 401
        return analyse.public_json(), 200
    except Exception as e:
        current_app.logger.info("error on get analyse " + str(e))
        return "bad request", 400


@bp.route("/analyse/<id>", methods=["DELETE"])
@token_required
def delete_analyse(id, token):
    analyse = Analyse.query.filter_by(id=id).first_or_404()
    try:
        if not "admin" in token.get("scope", None):
            if analyse.created_by != token.get("id", None):
                current_app.logger.warning(
                    f"user attempt to delete analyse he didn't create, user_id={token.get('id',None)}, analyse_id={id}"
                )
                return "not authorized", 401
        db.session.delete(analyse)
        db.session.commit()
        return "ok", 200
    except Exception as e:
        current_app.logger.info("error on delete analyse " + str(e))
        return "bad request", 400


@bp.route("/analyse/<id>/estimate", methods=["POST"])
@token_required
def estimate_analyse(id, token):
    data = request.get_json()
    if not "budget" in data:
        return "you have to provide a budget", 400
    if not "index" in data:
        return "you have to provide an index", 400
    analyse = db.session.query(Analyse).filter_by(id=id).first_or_404()
    try:
        if analyse.created_by != token.get("id", None):
            current_app.logger.warning(
                f"user attempt to estimate analyse he didn't create, user_id={token.get('id',None)}, analyse_id={id}"
            )
            return "not authorized", 401
        try:
            estimation = analyse.estimate(data["budget"], int(data["index"]))
        except Exception as e:
            current_app.logger.info("can't estimate analyse " + str(e))
            return f"can't estimate analyse because {e}", 400
        db.session.commit()
        return str(estimation), 200
    except Exception as e:
        current_app.logger.info("error on estimate analyse " + str(e))
        return "bad request", 400


@bp.route("/analyse/<id>/report", methods=["GET"])
@token_required
def get_report(id, token):
    analyse = Analyse.query.filter_by(id=id).first_or_404()
    try:
        return (
            analyse.generate_report(),
            200,
            {
                "Content-Type": "application/octet-stream",
                "Content-Disposition": "attachment; filename="
                + analyse.filename
                + "report.pdf",
            },
        )
    except Exception as e:
        current_app.logger.info("error on get analyse " + str(e))
        return "bad request", 400
