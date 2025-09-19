from werkzeug.security import generate_password_hash, check_password_hash
from store_application.models.store_model import Users
from store_application.db_session import ScopedSession
import logging

from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta


def register_user(username, mobile, email, password, user_group="customer"):
    local_session = ScopedSession()
    try:
        if user_group not in ['admin', 'customer']:
            user_group = 'customer'
        hashed_password = generate_password_hash(
            password, method="pbkdf2:sha256", salt_length=16)
        user = Users(username=username,
                      phone=mobile,
                      email=email,
                      password=hashed_password,
                      user_role=user_group
                      )
        local_session.add(user)
        local_session.commit()
        local_session.close()

        return True, user

    except Exception as e:
        logging.error("register_user_error", exc_info=e)
        return False, "Unable to create the account"
    



def login_user(email, password):
    local_session = ScopedSession()
    try:
        user = local_session.query(Users).filter_by(email=email).first()
                
        if user and check_password_hash(user.password, password):
            token_payload = {
                "user_id": str(user.id),
                "username": user.username,
                "user_role": user.user_role
            }
            access_token = create_access_token(
                identity = user.id,
                additional_claims=token_payload,
                expires_delta=timedelta(hours=24))
            refresh_token = create_refresh_token(
                identity = user.id,
                additional_claims=token_payload,
                expires_delta=timedelta(days=7))
            
            return True, {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

        return False, "Invalid username or password"

    except Exception as e:
        logging.error("login_user_error", exc_info=e)
        return False, "Unable to login"
