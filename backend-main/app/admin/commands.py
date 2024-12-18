from app.admin import cli
from app.extensions import db
from app.models.user import User
import click


@cli.cli.command("create-admin")
@click.option("--email", prompt="Email ", help="Email of the admin")
@click.option("--password", prompt="Password ", help="Password of the admin")
@click.option("--name", prompt="Name ", help="Name of the admin")
def create_user(email, password, name):
    user = User(
        email=email,
        password=password,
        name=name,
        _type="admin",
        email_verified=True,
        phone_verified=True,
    )
    db.session.add(user)
    db.session.commit()
    click.echo(f"Admin {user.email} created successfullly")


@cli.cli.command("modify-user-password")
@click.option("--email", prompt="Email ", help="User email")
@click.option("--password", prompt="Password ", help="New password")
def modify_user(email, password):
    user = User.query.filter_by(email=email).first()
    user.modify_password(password)
    db.session.commit()
    click.echo(f"User {user.email} password successfullly modified.")
