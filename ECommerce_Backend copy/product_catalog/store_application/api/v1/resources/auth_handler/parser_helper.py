from flask_restx import reqparse
import re
from werkzeug.exceptions import BadRequest


class StrongPasswordError(Exception):
    pass


def validate_strong_password(password: str) -> str:
    errors = []

    if len(password) < 8:
        errors.append("minimum 8 characters required")

    if re.search(r"\s", password):
        errors.append("spaces are not allowed")

    allowed_specials = r"@$!%*#?&"

    if not re.search(r"[a-z]", password):
        errors.append("at least 1 lowercase letter required")
    if not re.search(r"[A-Z]", password):
        errors.append("at least 1 uppercase letter required")
    if not re.search(r"[0-9]", password):
        errors.append("at least 1 digit required")
    if not re.search(f"[{re.escape(allowed_specials)}]", password):
        errors.append(
            f"at least 1 special character required ({allowed_specials})")

    if re.search(f"[^{re.escape(allowed_specials)}a-zA-Z0-9]", password):
        errors.append(
            f"only these special characters are allowed: {allowed_specials}")

    if errors:
        raise StrongPasswordError(
            "Weak password: " + "; ".join(errors)
        )

    return password


def phone_type(value: str) -> str:
    if not re.fullmatch(r"^\+91\d{10}$", value):
        raise BadRequest("Phone number must start with +91 and be followed by 10 digits")
    return value


signup_parser = reqparse.RequestParser(bundle_errors=True)
signup_parser.add_argument("username", type=str, location="json")
signup_parser.add_argument("mobile", type=phone_type, location="json")
signup_parser.add_argument("email", type=str, location="json")
signup_parser.add_argument("password",
                           type=lambda password: validate_strong_password(
                               password), location="json")
signup_parser.add_argument("user_group", type=str, location="json")


login_parser = reqparse.RequestParser(bundle_errors=True)
login_parser.add_argument("email", type=str, location="json")
login_parser.add_argument("password", location="json")
