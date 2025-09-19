from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt

def require_roles(*roles):
    """Protect endpoint and require one of the given roles via JWT custom claims."""
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("user_role")
            if role not in roles:
                return jsonify({
                    "message": "Forbidden",
                    "status": False,
                    "type": "forbidden"
                }), 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper

def require_auth(fn):
    """Protect endpoint (no role check)."""
    @wraps(fn)
    @jwt_required()
    def decorated(*args, **kwargs):
        return fn(*args, **kwargs)
    return decorated
