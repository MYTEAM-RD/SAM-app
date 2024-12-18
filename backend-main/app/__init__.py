from flask import Flask, Blueprint, send_from_directory
from flask_cors import CORS
from config import Config
from app.extensions import db
from app.extensions import migrate
import os
import stripe
from jinja2 import Environment, FileSystemLoader


def create_app(config_class=Config):
    # Create a Flask application object with the current module name
    app = Flask(__name__)
    app.config['SQLALCHEMY_ECHO'] = True

    # check if the app contains the needed configuration
    if os.environ.get("TEST_MODE", None) != "True":
        if os.environ.get("SMTP_HOST", None) == None:
            raise Exception(
                "Please set SMTP_HOST to production, set TEST_MODE to True if you want to use the development environment"
            )
        if os.environ.get("SMTP_USER", None) == None:
            raise Exception(
                "Please set SMTP_USER to production, set TEST_MODE to True if you want to use the development environment"
            )
        if os.environ.get("SMTP_PASSWORD", None) == None:
            raise Exception(
                "Please set SMTP_PASSWORD to production, set TEST_MODE to True if you want to use the development environment"
            )
        if os.environ.get("SMTP_PORT", None) == None:
            raise Exception(
                "Please set SMTP_PORT to production, set TEST_MODE to True if you want to use the development environment"
            )
        if os.environ.get("SECRET_KEY", None) == None:
            raise Exception(
                "Please set SECRET_KEY to production, set TEST_MODE to True if you want to use the development environment"
            )
        if os.environ.get("DATABASE_URI", None) == None:
            raise Exception(
                "Please set DATABASE_URI to production, set TEST_MODE to True if you want to use the development environment"
            )
        # optional configuration
        # if os.environ.get('DATABASE_URI',None) == None:
        #    app.logger.critical('\n\n WARNING !!!! : You should set DATABASE_URI on production environment\n\n')
        # if os.environ.get('CORS_ORIGINS',None) == None:
        #    app.logger.critical('\n\n WARNING !!!! : You should set CORS_ORIGINS on production environment\n\n')

    # Load the configuration options from the config_class object
    app.config.from_object(config_class)
    CORS(app, origins=os.environ.get("CORS_ORIGINS", "").split(";"))
    # Register Flask extensions
    # Initialize the database object with the Flask application
    db.init_app(app)
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
    # Import models to register them with the Flask application
    # from app.models.message import Message

    # Initialize the migration object with the Flask application and the database object
    migrate.init_app(app, db)

    main_route = Blueprint("main_route", __name__, url_prefix="/api/v1")

    # Register blueprints with the Flask application
    # Import blueprints and register them with the Flask application
    from app.user import bp as user_bp

    main_route.register_blueprint(user_bp)
    from app.analyse import bp as analyse_bp

    main_route.register_blueprint(analyse_bp)
    from app.verification import bp as verification_bp

    main_route.register_blueprint(verification_bp)
    from app.contact import bp as contact_bp

    main_route.register_blueprint(contact_bp)
    from app.payment import bp as payment_bp

    main_route.register_blueprint(payment_bp)

    # Register cli commands
    from app.admin import cli as admin_cli

    app.register_blueprint(admin_cli)

    # Register useful routes with the Flask application
    # Define a route for health checks
    @main_route.route("/health", methods=["GET"])
    def health():
        return "OK", 200

    swagger_bp = Blueprint("swagger", __name__)

    @swagger_bp.route("/swagger", methods=["GET"])
    def swagger():
        template_path = os.path.abspath(os.path.dirname(__file__)) + "/templates/pages"
        environment = Environment(loader=FileSystemLoader(template_path))
        template = environment.get_template("swagger.html")
        return template.render()

    @swagger_bp.route(rule="/openapi", methods=["GET"])
    def openapi():
        dir = os.path.dirname(os.path.abspath(__file__))
        return send_from_directory(
            os.path.dirname(os.path.abspath(__file__)),
            path="openapi.yml",
            as_attachment=True,
        )

    app.register_blueprint(main_route)
    if os.environ.get("SWAGGER", False):
        app.register_blueprint(swagger_bp)

    # security extra params
    app.jinja_env.autoescape = True

    # Return the Flask application object
    return app
