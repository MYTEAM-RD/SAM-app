from functools import wraps
import jwt
import os
from flask import request, current_app, request
from sqlalchemy import and_
from app.models.user import User


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            if len(token.split()) > 1:
                token = token.split()[1]
            else:
                return {"message": "Authorization Header is missing."}, 401
        if not token:
            return {"message": "Authorization Header is missing."}, 401
        try:
            data = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired."}, 401
        except jwt.InvalidTokenError:
            current_app.logger.warning(
                f"{request.remote_addr} [submitted an invalid token]"
            )
            return {"message": "Invalid token."}, 401
        # Pass the decoded token data to the wrapped function
        return f(token=data, *args, **kwargs)

    return decorated_function


def token_required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            if len(token.split()) > 1:
                token = token.split()[1]
            else:
                return {"message": "Authorization Header is missing."}, 401
        if not token:
            return {"message": "Authorization Header is missing."}, 401
        try:
            data = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
            if not "admin" in data["scope"]:
                return {"message": "Not authorized."}, 401
        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired."}, 401
        except jwt.InvalidTokenError:
            current_app.logger.warning(
                f"{request.remote_addr} [submitted an invalid token]"
            )
            return {"message": "Invalid token."}, 401
        except Exception as e:
            current_app.logger.warning(
                f"{request.remote_addr} [failed to login as admin]"
            )
            return {"message": "Failed to login as admin."}, 401
        # Pass the decoded token data to the wrapped function
        return f(token=data, *args, **kwargs)

    return decorated_function
